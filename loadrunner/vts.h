#ifndef VTS_H
#define VTS_H

/*
 * VTS Helper Library for LoadRunner
 * Mimics lrvtc_* functions but for the new REST API.
 */

char vts_base_url[1024];
char vts_key[256];

/**
 * Initialize VTS connection settings
 */
void vts_init(const char* url, const char* api_key) {
    strcpy(vts_base_url, url);
    strcpy(vts_key, api_key);
}

/**
 * Lease a record from a specific port.
 *
 * @param port_name Name of the VTS port
 * @param out_id_param Name of the LR parameter to store the Record ID
 * @param out_data_param Name of the LR parameter to store the JSON Data
 * @return 0 on success, -1 on failure (no records)
 */
int vts_lease_record(const char* port_name, const char* out_id_param, const char* out_data_param) {
    char full_url[2048];
    sprintf(full_url, "%s/api/ports/%s/records/lease", vts_base_url, port_name);

    web_add_header("X-API-Key", vts_key);
    web_add_header("Content-Type", "application/json");

    // Save Record ID
    web_reg_save_param_json(
        "ParamName=Internal_VTS_ID",
        "QueryString=$.recordId",
        "Notfound=warning",
        SEARCH_FILTERS,
        "Scope=Body",
        LAST);

    // Save Data
    web_reg_save_param_json(
        "ParamName=Internal_VTS_Data",
        "QueryString=$.data",
        "Notfound=warning",
        SEARCH_FILTERS,
        "Scope=Body",
        LAST);

    int rc = web_custom_request("VTS_Lease",
        "URL", full_url,
        "Method=POST",
        "Resource=0",
        "RecContentType=application/json",
        "Body=",
        LAST);

    if (rc == LR_PASS) {
        // Check if we got data
        const char* id = lr_eval_string("{Internal_VTS_ID}");
        if (id && strlen(id) > 0 && strcmp(id, "{Internal_VTS_ID}") != 0) {
            lr_save_string(id, out_id_param);
            lr_save_string(lr_eval_string("{Internal_VTS_Data}"), out_data_param);
            return 0;
        }
    }

    return -1;
}

/**
 * Consume a record (mark as used).
 *
 * @param record_id The ID of the record to consume
 */
void vts_consume_record(const char* record_id) {
    char full_url[2048];
    sprintf(full_url, "%s/api/records/%s/consume", vts_base_url, record_id);

    web_add_header("X-API-Key", vts_key);

    web_custom_request("VTS_Consume",
        "URL", full_url,
        "Method=POST",
        "Resource=0",
        "Body=",
        LAST);
}

/**
 * Release a record (return to available).
 *
 * @param record_id The ID of the record to release
 */
void vts_release_record(const char* record_id) {
    char full_url[2048];
    sprintf(full_url, "%s/api/records/%s/release", vts_base_url, record_id);

    web_add_header("X-API-Key", vts_key);

    web_custom_request("VTS_Release",
        "URL", full_url,
        "Method=POST",
        "Resource=0",
        "Body=",
        LAST);
}

#endif // VTS_H
