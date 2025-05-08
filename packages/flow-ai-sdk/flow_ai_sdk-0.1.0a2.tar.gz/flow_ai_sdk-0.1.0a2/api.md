# API

## V1

Types:

```python
from flow_ai_sdk.types.api import (
    V1GetValidationTaskStatusResponse,
    V1HandleClerkWebhookResponse,
    V1RootResponse,
)
```

Methods:

- <code title="get /api/v1/validation-tasks/{validation_task_id}">client.api.v1.<a href="./src/flow_ai_sdk/resources/api/v1/v1.py">get_validation_task_status</a>(validation_task_id) -> <a href="./src/flow_ai_sdk/types/api/v1_get_validation_task_status_response.py">object</a></code>
- <code title="post /api/v1/clerk-webhooks">client.api.v1.<a href="./src/flow_ai_sdk/resources/api/v1/v1.py">handle_clerk_webhook</a>() -> <a href="./src/flow_ai_sdk/types/api/v1_handle_clerk_webhook_response.py">object</a></code>
- <code title="get /api/v1">client.api.v1.<a href="./src/flow_ai_sdk/resources/api/v1/v1.py">root</a>() -> <a href="./src/flow_ai_sdk/types/api/v1_root_response.py">object</a></code>

### Health

Types:

```python
from flow_ai_sdk.types.api.v1 import HealthCheckResponse, HealthCheckDBResponse
```

Methods:

- <code title="get /api/v1/health/">client.api.v1.health.<a href="./src/flow_ai_sdk/resources/api/v1/health.py">check</a>() -> <a href="./src/flow_ai_sdk/types/api/v1/health_check_response.py">object</a></code>
- <code title="get /api/v1/health/db">client.api.v1.health.<a href="./src/flow_ai_sdk/resources/api/v1/health.py">check_db</a>() -> <a href="./src/flow_ai_sdk/types/api/v1/health_check_db_response.py">object</a></code>

### Users

#### Me

Types:

```python
from flow_ai_sdk.types.api.v1.users import UserRead, MeGetBasicInfoResponse
```

Methods:

- <code title="get /api/v1/users/me">client.api.v1.users.me.<a href="./src/flow_ai_sdk/resources/api/v1/users/me.py">retrieve</a>() -> <a href="./src/flow_ai_sdk/types/api/v1/users/user_read.py">UserRead</a></code>
- <code title="patch /api/v1/users/me">client.api.v1.users.me.<a href="./src/flow_ai_sdk/resources/api/v1/users/me.py">update</a>(\*\*<a href="src/flow_ai_sdk/types/api/v1/users/me_update_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/api/v1/users/user_read.py">UserRead</a></code>
- <code title="get /api/v1/users/me/basic-info">client.api.v1.users.me.<a href="./src/flow_ai_sdk/resources/api/v1/users/me.py">get_basic_info</a>() -> <a href="./src/flow_ai_sdk/types/api/v1/users/me_get_basic_info_response.py">object</a></code>

### TestCases

Types:

```python
from flow_ai_sdk.types.api.v1 import (
    TestCaseRead,
    TestCaseListResponse,
    TestCaseGetValidationResponse,
)
```

Methods:

- <code title="post /api/v1/test-cases/">client.api.v1.test_cases.<a href="./src/flow_ai_sdk/resources/api/v1/test_cases.py">create</a>(\*\*<a href="src/flow_ai_sdk/types/api/v1/test_case_create_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/api/v1/test_case_read.py">TestCaseRead</a></code>
- <code title="get /api/v1/test-cases/{test_case_id}">client.api.v1.test_cases.<a href="./src/flow_ai_sdk/resources/api/v1/test_cases.py">retrieve</a>(test_case_id) -> <a href="./src/flow_ai_sdk/types/api/v1/test_case_read.py">TestCaseRead</a></code>
- <code title="put /api/v1/test-cases/{test_case_id}">client.api.v1.test_cases.<a href="./src/flow_ai_sdk/resources/api/v1/test_cases.py">update</a>(test_case_id, \*\*<a href="src/flow_ai_sdk/types/api/v1/test_case_update_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/api/v1/test_case_read.py">TestCaseRead</a></code>
- <code title="get /api/v1/test-cases/">client.api.v1.test_cases.<a href="./src/flow_ai_sdk/resources/api/v1/test_cases.py">list</a>(\*\*<a href="src/flow_ai_sdk/types/api/v1/test_case_list_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/api/v1/test_case_list_response.py">TestCaseListResponse</a></code>
- <code title="delete /api/v1/test-cases/{test_case_id}">client.api.v1.test_cases.<a href="./src/flow_ai_sdk/resources/api/v1/test_cases.py">delete</a>(test_case_id) -> None</code>
- <code title="get /api/v1/test-cases/{test_case_id}/validation">client.api.v1.test_cases.<a href="./src/flow_ai_sdk/resources/api/v1/test_cases.py">get_validation</a>(test_case_id) -> <a href="./src/flow_ai_sdk/types/api/v1/test_case_get_validation_response.py">object</a></code>

### Validations

Types:

```python
from flow_ai_sdk.types.api.v1 import (
    TestCaseValidationRead,
    ValidationItemFeedbackInput,
    ValidationListResponse,
)
```

Methods:

- <code title="post /api/v1/validations">client.api.v1.validations.<a href="./src/flow_ai_sdk/resources/api/v1/validations.py">create</a>(\*\*<a href="src/flow_ai_sdk/types/api/v1/validation_create_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/api/v1/test_case_validation_read.py">TestCaseValidationRead</a></code>
- <code title="get /api/v1/validations/{validation_id}">client.api.v1.validations.<a href="./src/flow_ai_sdk/resources/api/v1/validations.py">retrieve</a>(validation_id) -> <a href="./src/flow_ai_sdk/types/api/v1/test_case_validation_read.py">TestCaseValidationRead</a></code>
- <code title="put /api/v1/validations/{validation_id}">client.api.v1.validations.<a href="./src/flow_ai_sdk/resources/api/v1/validations.py">update</a>(validation_id, \*\*<a href="src/flow_ai_sdk/types/api/v1/validation_update_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/api/v1/test_case_validation_read.py">TestCaseValidationRead</a></code>
- <code title="get /api/v1/validations">client.api.v1.validations.<a href="./src/flow_ai_sdk/resources/api/v1/validations.py">list</a>(\*\*<a href="src/flow_ai_sdk/types/api/v1/validation_list_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/api/v1/validation_list_response.py">ValidationListResponse</a></code>
- <code title="delete /api/v1/validations/{validation_id}">client.api.v1.validations.<a href="./src/flow_ai_sdk/resources/api/v1/validations.py">delete</a>(validation_id) -> None</code>

### Batches

Types:

```python
from flow_ai_sdk.types.api.v1 import (
    BatchRead,
    BatchCreateValidationTaskResponse,
    BatchGetValidationTaskResponse,
    BatchListByAPIKeyResponse,
    BatchListMineResponse,
    BatchListTestCasesResponse,
    BatchListValidationsResponse,
)
```

Methods:

- <code title="post /api/v1/batches/">client.api.v1.batches.<a href="./src/flow_ai_sdk/resources/api/v1/batches.py">create</a>(\*\*<a href="src/flow_ai_sdk/types/api/v1/batch_create_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/api/v1/batch_read.py">BatchRead</a></code>
- <code title="get /api/v1/batches/{batch_id}">client.api.v1.batches.<a href="./src/flow_ai_sdk/resources/api/v1/batches.py">retrieve</a>(batch_id) -> <a href="./src/flow_ai_sdk/types/api/v1/batch_read.py">BatchRead</a></code>
- <code title="delete /api/v1/batches/{batch_id}">client.api.v1.batches.<a href="./src/flow_ai_sdk/resources/api/v1/batches.py">delete</a>(batch_id) -> None</code>
- <code title="post /api/v1/batches/{batch_id}/validation-tasks">client.api.v1.batches.<a href="./src/flow_ai_sdk/resources/api/v1/batches.py">create_validation_task</a>(batch_id) -> <a href="./src/flow_ai_sdk/types/api/v1/batch_create_validation_task_response.py">object</a></code>
- <code title="get /api/v1/batches/{batch_id}/validation-task">client.api.v1.batches.<a href="./src/flow_ai_sdk/resources/api/v1/batches.py">get_validation_task</a>(batch_id) -> <a href="./src/flow_ai_sdk/types/api/v1/batch_get_validation_task_response.py">object</a></code>
- <code title="get /api/v1/batches/by_api_key">client.api.v1.batches.<a href="./src/flow_ai_sdk/resources/api/v1/batches.py">list_by_api_key</a>() -> <a href="./src/flow_ai_sdk/types/api/v1/batch_list_by_api_key_response.py">BatchListByAPIKeyResponse</a></code>
- <code title="get /api/v1/batches/mine">client.api.v1.batches.<a href="./src/flow_ai_sdk/resources/api/v1/batches.py">list_mine</a>() -> <a href="./src/flow_ai_sdk/types/api/v1/batch_list_mine_response.py">BatchListMineResponse</a></code>
- <code title="get /api/v1/batches/{batch_id}/testcases">client.api.v1.batches.<a href="./src/flow_ai_sdk/resources/api/v1/batches.py">list_test_cases</a>(batch_id) -> <a href="./src/flow_ai_sdk/types/api/v1/batch_list_test_cases_response.py">BatchListTestCasesResponse</a></code>
- <code title="get /api/v1/batches/{batch_id}/validations">client.api.v1.batches.<a href="./src/flow_ai_sdk/resources/api/v1/batches.py">list_validations</a>(batch_id) -> <a href="./src/flow_ai_sdk/types/api/v1/batch_list_validations_response.py">BatchListValidationsResponse</a></code>

### Keys

Types:

```python
from flow_ai_sdk.types.api.v1 import APIKeyCreate, APIKeyInfo, KeyListResponse
```

Methods:

- <code title="post /api/v1/keys">client.api.v1.keys.<a href="./src/flow_ai_sdk/resources/api/v1/keys.py">create</a>(\*\*<a href="src/flow_ai_sdk/types/api/v1/key_create_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/api/v1/api_key_create.py">APIKeyCreate</a></code>
- <code title="get /api/v1/keys">client.api.v1.keys.<a href="./src/flow_ai_sdk/resources/api/v1/keys.py">list</a>() -> <a href="./src/flow_ai_sdk/types/api/v1/key_list_response.py">KeyListResponse</a></code>
- <code title="delete /api/v1/keys/{key_id}">client.api.v1.keys.<a href="./src/flow_ai_sdk/resources/api/v1/keys.py">revoke</a>(key_id) -> None</code>

### Auth

#### SDK

Methods:

- <code title="post /api/v1/auth/sdk/login">client.api.v1.auth.sdk.<a href="./src/flow_ai_sdk/resources/api/v1/auth/sdk.py">login</a>() -> <a href="./src/flow_ai_sdk/types/api/v1/api_key_create.py">APIKeyCreate</a></code>

#### Validators

Types:

```python
from flow_ai_sdk.types.api.v1.auth import (
    ValidatorCompleteSignupResponse,
    ValidatorVerifyAccessResponse,
)
```

Methods:

- <code title="post /api/v1/auth/validators/complete-signup">client.api.v1.auth.validators.<a href="./src/flow_ai_sdk/resources/api/v1/auth/validators.py">complete_signup</a>(\*\*<a href="src/flow_ai_sdk/types/api/v1/auth/validator_complete_signup_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/api/v1/auth/validator_complete_signup_response.py">object</a></code>
- <code title="post /api/v1/auth/validators/verify-access">client.api.v1.auth.validators.<a href="./src/flow_ai_sdk/resources/api/v1/auth/validators.py">verify_access</a>(\*\*<a href="src/flow_ai_sdk/types/api/v1/auth/validator_verify_access_params.py">params</a>) -> <a href="./src/flow_ai_sdk/types/api/v1/auth/validator_verify_access_response.py">object</a></code>

### Datasets

Types:

```python
from flow_ai_sdk.types.api.v1 import DatasetGetItemsResponse
```

Methods:

- <code title="delete /api/v1/datasets/{dataset_id}">client.api.v1.datasets.<a href="./src/flow_ai_sdk/resources/api/v1/datasets.py">delete_dataset</a>(dataset_id) -> None</code>
- <code title="get /api/v1/datasets/{dataset_id}/items">client.api.v1.datasets.<a href="./src/flow_ai_sdk/resources/api/v1/datasets.py">get_items</a>(dataset_id) -> <a href="./src/flow_ai_sdk/types/api/v1/dataset_get_items_response.py">object</a></code>

### Jobs

Types:

```python
from flow_ai_sdk.types.api.v1 import (
    JobCancelResponse,
    JobGenerateBatchResponse,
    JobGenerateDatasetResponse,
    JobGetDetailsResponse,
    JobListBatchesResponse,
)
```

Methods:

- <code title="post /api/v1/jobs/{job_id}/cancel">client.api.v1.jobs.<a href="./src/flow_ai_sdk/resources/api/v1/jobs.py">cancel</a>(job_id) -> <a href="./src/flow_ai_sdk/types/api/v1/job_cancel_response.py">object</a></code>
- <code title="post /api/v1/jobs/{job_id}/generate-batch">client.api.v1.jobs.<a href="./src/flow_ai_sdk/resources/api/v1/jobs.py">generate_batch</a>(job_id) -> <a href="./src/flow_ai_sdk/types/api/v1/job_generate_batch_response.py">object</a></code>
- <code title="post /api/v1/jobs/{job_id}/generate-dataset">client.api.v1.jobs.<a href="./src/flow_ai_sdk/resources/api/v1/jobs.py">generate_dataset</a>(job_id) -> <a href="./src/flow_ai_sdk/types/api/v1/job_generate_dataset_response.py">object</a></code>
- <code title="get /api/v1/jobs/{job_id}">client.api.v1.jobs.<a href="./src/flow_ai_sdk/resources/api/v1/jobs.py">get_details</a>(job_id) -> <a href="./src/flow_ai_sdk/types/api/v1/job_get_details_response.py">object</a></code>
- <code title="get /api/v1/jobs/{job_id}/batches">client.api.v1.jobs.<a href="./src/flow_ai_sdk/resources/api/v1/jobs.py">list_batches</a>(job_id) -> <a href="./src/flow_ai_sdk/types/api/v1/job_list_batches_response.py">object</a></code>

### Projects

Types:

```python
from flow_ai_sdk.types.api.v1 import (
    ProjectCreateResponse,
    ProjectUpdateResponse,
    ProjectListResponse,
    ProjectArchiveResponse,
    ProjectGetResponse,
    ProjectGetDatasetResponse,
    ProjectListDatasetVersionsResponse,
)
```

Methods:

- <code title="post /api/v1/projects/">client.api.v1.projects.<a href="./src/flow_ai_sdk/resources/api/v1/projects/projects.py">create</a>() -> <a href="./src/flow_ai_sdk/types/api/v1/project_create_response.py">object</a></code>
- <code title="patch /api/v1/projects/{project_id}">client.api.v1.projects.<a href="./src/flow_ai_sdk/resources/api/v1/projects/projects.py">update</a>(project_id) -> <a href="./src/flow_ai_sdk/types/api/v1/project_update_response.py">object</a></code>
- <code title="get /api/v1/projects/">client.api.v1.projects.<a href="./src/flow_ai_sdk/resources/api/v1/projects/projects.py">list</a>() -> <a href="./src/flow_ai_sdk/types/api/v1/project_list_response.py">object</a></code>
- <code title="delete /api/v1/projects/{project_id}">client.api.v1.projects.<a href="./src/flow_ai_sdk/resources/api/v1/projects/projects.py">delete</a>(project_id) -> None</code>
- <code title="post /api/v1/projects/{project_id}/archive">client.api.v1.projects.<a href="./src/flow_ai_sdk/resources/api/v1/projects/projects.py">archive</a>(project_id) -> <a href="./src/flow_ai_sdk/types/api/v1/project_archive_response.py">object</a></code>
- <code title="get /api/v1/projects/{project_id}">client.api.v1.projects.<a href="./src/flow_ai_sdk/resources/api/v1/projects/projects.py">get</a>(project_id) -> <a href="./src/flow_ai_sdk/types/api/v1/project_get_response.py">object</a></code>
- <code title="get /api/v1/projects/{project_id}/dataset">client.api.v1.projects.<a href="./src/flow_ai_sdk/resources/api/v1/projects/projects.py">get_dataset</a>(project_id) -> <a href="./src/flow_ai_sdk/types/api/v1/project_get_dataset_response.py">object</a></code>
- <code title="get /api/v1/projects/{project_id}/datasets">client.api.v1.projects.<a href="./src/flow_ai_sdk/resources/api/v1/projects/projects.py">list_dataset_versions</a>(project_id) -> <a href="./src/flow_ai_sdk/types/api/v1/project_list_dataset_versions_response.py">object</a></code>

#### Jobs

Types:

```python
from flow_ai_sdk.types.api.v1.projects import JobCreateResponse, JobListResponse
```

Methods:

- <code title="post /api/v1/projects/{project_id}/jobs">client.api.v1.projects.jobs.<a href="./src/flow_ai_sdk/resources/api/v1/projects/jobs.py">create</a>(project_id) -> <a href="./src/flow_ai_sdk/types/api/v1/projects/job_create_response.py">object</a></code>
- <code title="get /api/v1/projects/{project_id}/jobs">client.api.v1.projects.jobs.<a href="./src/flow_ai_sdk/resources/api/v1/projects/jobs.py">list</a>(project_id) -> <a href="./src/flow_ai_sdk/types/api/v1/projects/job_list_response.py">object</a></code>

#### Validators

Types:

```python
from flow_ai_sdk.types.api.v1.projects import ValidatorAddResponse, ValidatorRemoveResponse
```

Methods:

- <code title="post /api/v1/projects/{project_id}/validators">client.api.v1.projects.validators.<a href="./src/flow_ai_sdk/resources/api/v1/projects/validators.py">add</a>(project_id) -> <a href="./src/flow_ai_sdk/types/api/v1/projects/validator_add_response.py">object</a></code>
- <code title="delete /api/v1/projects/{project_id}/validators/{validator_id}">client.api.v1.projects.validators.<a href="./src/flow_ai_sdk/resources/api/v1/projects/validators.py">remove</a>(validator_id, \*, project_id) -> <a href="./src/flow_ai_sdk/types/api/v1/projects/validator_remove_response.py">object</a></code>

### ValidatorTasks

Types:

```python
from flow_ai_sdk.types.api.v1 import ValidatorTaskGetTestCasesResponse, ValidatorTaskSubmitResponse
```

Methods:

- <code title="get /api/v1/validator-tasks/{validator_task_id}/test-cases">client.api.v1.validator_tasks.<a href="./src/flow_ai_sdk/resources/api/v1/validator_tasks/validator_tasks.py">get_test_cases</a>(validator_task_id) -> <a href="./src/flow_ai_sdk/types/api/v1/validator_task_get_test_cases_response.py">object</a></code>
- <code title="post /api/v1/validator-tasks/{validator_task_id}/submit">client.api.v1.validator_tasks.<a href="./src/flow_ai_sdk/resources/api/v1/validator_tasks/validator_tasks.py">submit</a>(validator_task_id) -> <a href="./src/flow_ai_sdk/types/api/v1/validator_task_submit_response.py">object</a></code>

#### Validations

Types:

```python
from flow_ai_sdk.types.api.v1.validator_tasks import (
    ValidationEditResponse,
    ValidationSubmitResponse,
)
```

Methods:

- <code title="put /api/v1/validator-tasks/{validator_task_id}/validations/{validation_id}">client.api.v1.validator_tasks.validations.<a href="./src/flow_ai_sdk/resources/api/v1/validator_tasks/validations.py">edit</a>(validation_id, \*, validator_task_id) -> <a href="./src/flow_ai_sdk/types/api/v1/validator_tasks/validation_edit_response.py">object</a></code>
- <code title="post /api/v1/validator-tasks/{validator_task_id}/validations">client.api.v1.validator_tasks.validations.<a href="./src/flow_ai_sdk/resources/api/v1/validator_tasks/validations.py">submit</a>(validator_task_id) -> <a href="./src/flow_ai_sdk/types/api/v1/validator_tasks/validation_submit_response.py">object</a></code>
