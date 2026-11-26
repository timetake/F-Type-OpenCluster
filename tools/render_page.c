#include "../page/page.h"

#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int read_config(const char *path, OcPage *page) {
    FILE *file = fopen(path, "rb");
    if (!file) { perror(path); return 0; }
    char data[OC_CONFIG_MAX + 1];
    size_t size = fread(data, 1, sizeof data, file);
    const char *error = ferror(file) ? "cannot read page" : oc_parse(data, size, page);
    fclose(file);
    if (error) fprintf(stderr, "%s: %s\n", path, error);
    return error == NULL;
}

static int read_usb_page(const char *root, OcPage *page) {
    const char suffix[] = "/OPENCLUSTER/PAGE.CFG";
    size_t path_size = strlen(root) + sizeof suffix;
    char *path = malloc(path_size);
    if (!path) { perror("page path"); return 0; }
    snprintf(path, path_size, "%s%s", root, suffix);
    int ok = read_config(path, page);
    free(path);
    return ok;
}

static int read_value(char *argument, OcReading *values) {
    char *value = strchr(argument, '=');
    if (!value) return 0;
    *value++ = 0;
    int index = oc_metric_index(argument);
    if (index < 0) return 0;
    char *end;
    errno = 0;
    long n = strtol(value, &end, 10);
    if (value == end || *end || errno == ERANGE || n < INT_MIN || n > INT_MAX) return 0;
    values[index] = (OcReading){1, (int)n};
    return 1;
}

int main(int argc, char **argv) {
    OcPage page;
    if (argc == 3 && !strcmp(argv[1], "--check")) return read_config(argv[2], &page) ? 0 : 1;
    if (argc < 3) {
        fprintf(stderr, "usage: render_page USB_ROOT OUTPUT.ppm [rpm=3200 oil_f=208 ...]\n");
        return 2;
    }
    if (!read_usb_page(argv[1], &page)) return 1;
    OcReading values[OC_METRIC_COUNT] = {{0}};
    for (int i = 3; i < argc; ++i) {
        if (!read_value(argv[i], values)) {
            fprintf(stderr, "invalid reading at argument %d\n", i);
            return 2;
        }
    }
    static OcFrame frame;
    oc_render(&page, values, frame);
    FILE *output = fopen(argv[2], "wb");
    if (!output) { perror(argv[2]); return 1; }
    int ok = fprintf(output, "P6\n%d %d\n255\n", OC_WIDTH, OC_HEIGHT) > 0 &&
             fwrite(frame, 1, sizeof frame, output) == sizeof frame;
    if (fclose(output) || !ok) { perror(argv[2]); return 1; }
    return 0;
}
