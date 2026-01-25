#include "vts.h"

vuser_init()
{
    // Initialize VTS connection
    // Replace with your actual VTS server URL and API Key
    vts_init("http://vts-server:3000", "secret-key-123");
    return 0;
}

Action()
{
    int rc;

    lr_start_transaction("VTS_Get_Data");

    // Lease a record from 'test-port'
    // Data will be stored in {MyRecordData}
    // Record ID will be stored in {MyRecordID}
    rc = vts_lease_record("test-port", "MyRecordID", "MyRecordData");

    if (rc == 0) {
        lr_end_transaction("VTS_Get_Data", LR_PASS);

        lr_output_message("Leased Record ID: %s", lr_eval_string("{MyRecordID}"));
        lr_output_message("Data: %s", lr_eval_string("{MyRecordData}"));

        // ... Use the data in your business process ...
        // web_url("Login", "URL=http://example.com?user={MyRecordData.username}", LAST);

        // Mark as consumed when done
        vts_consume_record(lr_eval_string("{MyRecordID}"));
    } else {
        lr_end_transaction("VTS_Get_Data", LR_FAIL);
        lr_error_message("No VTS data available!");
        return -1;
    }

    return 0;
}

vuser_end()
{
    return 0;
}
