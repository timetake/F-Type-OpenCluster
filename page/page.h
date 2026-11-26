#ifndef OPENCLUSTER_PAGE_H
#define OPENCLUSTER_PAGE_H

#include <stddef.h>
#include <stdint.h>

/* Logical canvas in RGB888. The host chooses where and how to present it. */
enum { OC_WIDTH = 400, OC_HEIGHT = 224, OC_CONFIG_MAX = 512 };
typedef uint8_t OcFrame[OC_HEIGHT][OC_WIDTH][3];

enum OcMetric { OC_RPM, OC_THROTTLE, OC_OIL_F, OC_COOLANT_F, OC_METRIC_COUNT };
typedef struct {
    char title[19];
    int rows;
    uint32_t accent;
    enum OcMetric primary, secondary;
} OcPage;

typedef struct {
    int available;
    int value;
} OcReading;

/* Returns NULL on success. An invalid config leaves the current page intact. */
const char *oc_parse(const char *bytes, size_t size, OcPage *page);
int oc_metric_index(const char *name);
void oc_render(const OcPage *page, const OcReading readings[OC_METRIC_COUNT], OcFrame frame);

#endif
