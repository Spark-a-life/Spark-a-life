# Security

Do not commit passwords, API keys, OAuth client secrets, access tokens, identity documents,
protected health information, unredacted participant/client data, facility security details,
or safety-critical procedures not approved for the environment.

This repository must not contain client records, CVs, opportunity corpora, case files,
or Witness dumps of real activity.

The Action Gateway, when implemented, must use least privilege, server-side authorisation
and explicit secret management. This snapshot does not implement a gateway.

Report suspected credential exposure by revoking the credential first, then recording the
incident through the appropriate Human Captain or organisational security process.
