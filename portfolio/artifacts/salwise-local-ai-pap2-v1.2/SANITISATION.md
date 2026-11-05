# Sanitisation note

The vendored `package/` bytes match the uploaded zip. Nothing was rewritten, so the Salwise checker and manifest remain replayable.

## What was scanned

- No private keys, bearer tokens, passwords, or `.env` secrets.
- No live client records. Cedar Learning is labelled fictional.
- Named person: Dr William Siew / Will, the stated owner, already present in the AIOS snapshot identity note.

## What is not portable

`package/Salwise_Local_AI_Sources_and_Reuse_v1.2.md` contains ChatGPT library URLs of the form:

`https://chatgpt.com/library?file_id=libfile_<id>&account_id=personal`

These identify files in a personal ChatGPT library. They are not credentials. They will not work for another account. They should be replaced with titles-only citations before any public GitHub profile publication.

Source SAL-Q checks mention "Stage and Studio" and quotation-to-invoice operability. Those are source-register obligations marked `NOT_ASSESSED` and explicitly not imported as corporate gates. They are not client data.

## Public-drop rule

If this package is ever copied to a public surface:

1. Redact `account_id=personal` library URLs.
2. Keep All Rights Reserved unless the owner issues a different licence.
3. Keep `runtime_status: NOT_ASSESSED`.
4. Do not add opportunity corpora, CVs, or hardware serials.
