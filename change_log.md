**0.3.3**
Pushed the component to ECR, tested out.
Small changes to documentation.

**0.3.2**
Fixed wrong links in documentation.
Added row logging after 500 requests.

**0.3.1**
Removed feature, which would write documents to `documents` table event when error occured. Fine-tuned category classification and added skip mechanism for category to prevent duplicate messages in `errors` table.
Added error category to `errors` to be able to better identify source of errors.
Added sample configuration to the component, as well as descriptions and README.
Small changes to overall code structure.

**0.3.0**
Completely reworked source code that now utilizes KBC library.
All of the requests are sent as one batch request with features and all is returned as a single call. Added retry mechanism for 403 errors (`rateLimitExceeded` or `dailyLimitExceeded`) and added retry for 400 error when using `classifyText` endpoint.