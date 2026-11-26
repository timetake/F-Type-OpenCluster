#include "page.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const struct { const char *id, *label, *unit; } metrics[] = {
    {"rpm", "ENGINE", "RPM"}, {"throttle_pct", "THROTTLE", "%"},
    {"oil_f", "OIL TEMP", "DEG F"}, {"coolant_f", "COOLANT", "DEG F"}
};

int oc_metric_index(const char *name) {
    for (int i = 0; i < OC_METRIC_COUNT; ++i)
        if (strcmp(name, metrics[i].id) == 0) return i;
    return -1;
}

const char *oc_parse(const char *bytes, size_t size, OcPage *page) {
    char buf[OC_CONFIG_MAX + 1];
    if (size > OC_CONFIG_MAX || memchr(bytes, 0, size)) return "invalid config size or embedded NUL";
    memcpy(buf, bytes, size);
    buf[size] = 0;
    OcPage next = {0};
    unsigned seen = 0;
    char *line = buf;
    while (line) {
        char *end = strchr(line, '\n');
        if (end) *end++ = 0;
        size_t len = strlen(line);
        if (len && line[len - 1] == '\r') line[--len] = 0;
        if (len) {
            char *value = strchr(line, '=');
            if (!value) return "expected key=value";
            *value++ = 0;
            unsigned field;
            if (strcmp(line, "title") == 0) {
                field = 1;
                size_t n = strlen(value);
                if (!n || n >= sizeof next.title || strspn(value, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -") != n
                    || strspn(value, " ") == n) return "title must be 1-18 characters: A-Z, digits, space or hyphen";
                memcpy(next.title, value, n + 1);
            } else if (strcmp(line, "layout") == 0) {
                field = 2;
                next.rows = strcmp(value, "rows") == 0;
                if (!next.rows && strcmp(value, "columns")) return "layout must be rows or columns";
            } else if (strcmp(line, "accent") == 0) {
                field = 4;
                if (strlen(value) != 6 || strspn(value, "0123456789abcdefABCDEF") != 6)
                    return "accent must contain six hexadecimal digits";
                next.accent = (uint32_t)strtoul(value, NULL, 16);
            } else if (strcmp(line, "primary") == 0 || strcmp(line, "secondary") == 0) {
                int metric = oc_metric_index(value);
                if (metric < 0) return "unknown metric";
                field = strcmp(line, "primary") == 0 ? 8u : 16u;
                if (field == 8) next.primary = (enum OcMetric)metric;
                else next.secondary = (enum OcMetric)metric;
            } else return "unknown page setting";
            if (seen & field) return "duplicate page setting";
            seen |= field;
        }
        line = end;
    }
    if (seen != 31) return "missing page setting";
    *page = next;
    return NULL;
}

/* Each row is five pixels, stored from left to right in bits 4 through 0. */
static const char alphabet[] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-%";
static const uint8_t letters[][7] = {
    {14,17,19,21,25,17,14},{4,12,4,4,4,4,14},{14,17,1,2,4,8,31},
    {30,1,1,14,1,1,30},{2,6,10,18,31,2,2},{31,16,16,30,1,1,30},
    {6,8,16,30,17,17,14},{31,1,2,4,8,8,8},{14,17,17,14,17,17,14},
    {14,17,17,15,1,2,12},
    {14,17,17,31,17,17,17},{30,17,17,30,17,17,30},{15,16,16,16,16,16,15},
    {28,18,17,17,17,18,28},{31,16,16,30,16,16,31},{31,16,16,30,16,16,16},
    {15,16,16,23,17,17,15},{17,17,17,31,17,17,17},{14,4,4,4,4,4,14},
    {7,2,2,2,2,18,12},{17,18,20,24,20,18,17},{16,16,16,16,16,16,31},
    {17,27,21,21,17,17,17},{17,25,25,21,19,19,17},{14,17,17,17,17,17,14},
    {30,17,17,30,16,16,16},{14,17,17,17,21,18,13},{30,17,17,30,20,18,17},
    {15,16,16,14,1,1,30},{31,4,4,4,4,4,4},{17,17,17,17,17,17,14},
    {17,17,17,17,17,10,4},{17,17,17,21,21,27,17},{17,17,10,4,10,17,17},
    {17,17,10,4,4,4,4},{31,1,2,4,8,16,31},{0,0,0,31,0,0,0},{25,26,2,4,8,11,19}
};

static void rect(OcFrame frame, int x, int y, int w, int h, uint32_t color) {
    for (int j = y; j < y + h; ++j) {
        for (int i = x; i < x + w; ++i) {
            uint8_t *pixel = frame[j][i];
            pixel[0] = (uint8_t)(color >> 16);
            pixel[1] = (uint8_t)(color >> 8);
            pixel[2] = (uint8_t)color;
        }
    }
}

static void text(OcFrame frame, int x, int y, int scale, const char *s, uint32_t color) {
    for (; *s; ++s, x += 6 * scale) {
        const char *letter = strchr(alphabet, *s);
        if (!letter) continue;
        const uint8_t *glyph = letters[letter - alphabet];
        for (int row = 0; row < 7; ++row)
            for (int col = 0; col < 5; ++col)
                if (glyph[row] & (16 >> col))
                    rect(frame, x + col * scale, y + row * scale, scale, scale, color);
    }
}

static void metric_tile(OcFrame frame, int x, int y, int w, int h, enum OcMetric metric,
                        OcReading reading, uint32_t accent, int rows) {
    const uint32_t muted = 0xA3AFB7, white = 0xF4F6F8;
    char number[32] = "--";
    if (reading.available) snprintf(number, sizeof number, "%d", reading.value);
    int scale = rows ? 5 : 6;
    int value_width = rows ? w / 2 : w - 24;
    while (scale > 1 && (int)strlen(number) * 6 * scale > value_width) --scale;
    rect(frame, x, y, w, h, 0x19222A);
    rect(frame, x, y, 3, h, accent);
    text(frame, x + 14, y + 12, 2, metrics[metric].label, muted);
    text(frame, x + (rows ? w / 2 : 14), y + (rows ? 12 : 51), scale, number, white);
    text(frame, x + 14, y + h - 21, 2, metrics[metric].unit, accent);
}

void oc_render(const OcPage *page, const OcReading readings[OC_METRIC_COUNT], OcFrame frame) {
    rect(frame, 0, 0, OC_WIDTH, OC_HEIGHT, 0x0C1217);
    text(frame, 12, 12, 3, page->title, 0xF4F6F8);
    rect(frame, 12, 44, OC_WIDTH - 24, 2, page->accent);
    int w = page->rows ? 376 : 184;
    int h = page->rows ? 74 : 156;
    metric_tile(frame, 12, 56, w, h, page->primary, readings[page->primary], page->accent, page->rows);
    metric_tile(frame, page->rows ? 12 : 204, page->rows ? 138 : 56, w, h,
                page->secondary, readings[page->secondary], page->accent, page->rows);
}
