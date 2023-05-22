https://developer.microsoft.com/en-us/graph/graph-explorer


`https://graph.microsoft.com/v1.0/me/drive/recent`
```json
{
    "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#Collection(driveItem)",
    "value": [
        {
            "@odata.type": "#microsoft.graph.driveItem",
            "createdDateTime": "2023-05-10T08:42:09Z",
            "id": "{drive-item-id}",
            "lastModifiedDateTime": "2023-05-17T09:42:01Z",
            "name": "???.xlsx",
            "size": 82820,
            "webUrl": "???",
            "createdBy": {
                "user": {
                    "displayName": "???",
                    "email": "???"
                }
            },
            "lastModifiedBy": {
                "user": {
                    "displayName": "???",
                    "email": "???"
                }
            },
            "parentReference": {
                "driveId": "{drive-id}",
                "driveType": "documentLibrary",
                "id": "???"
            }
}]}
```

`range(address='A1:B2')`


`https://graph.microsoft.com/v1.0/drives/{drive-id}/items/{drive-item-id}/workbook/worksheets/SECONDARY/usedRange`
[ItemNotFound - Graph API Excel Workbook](https://learn.microsoft.com/en-us/answers/questions/1078833/itemnotfound-graph-api-excel-workbook)
`https://graph.microsoft.com/v1.0/drives/b!F87wNrhx-U2R67SLbwyMzTP0bdT7xwdCpJSjrjpCuCeMCTnJ7u8XTaCNnjrky1_j/items/01LNMZHYI2JQH3QAS44RFJLEYCA7KFD2U6/workbook/worksheets/SECONDARY/usedRange`



https://learn.microsoft.com/en-us/answers/questions/829998/about-microsoft-graph-api-get-onedrive-word-file-c


https://graph.microsoft.com/v1.0/drives/b!xMpu9J3Jl06Z0b5hV3pMAu66u-T3rW5Gk94KImBvVaK6NtC_PGLeTIZdPJBGttur/items/01PMKS4KLKGQIVQSI6KJGKYR5P5N533Z5D/content



https://stackoverflow.com/a/75201374/3356840
```bash
#! /usr/bin/bash

token=`curl \
    -d grant_type=client_credentials \
    -d client_id=[client_id] \
    -d client_secret=[client_secret] \
    -d scope=https://graph.microsoft.com/.default \
    -d resource=https://graph.microsoft.com \
    https://login.microsoftonline.com/[tenant_id]/oauth2/token \
    | jq -j .access_token`

curl -X GET \
    -H "Authorization: Bearer $token" \
    -H "Content-Type: application/json" \
    https://graph.microsoft.com/v1.0/groups \
    | jq .
```

curl -X GET -H "Authorization: Bearer $token" -H "Content-Type: application/json" 'https://graph.microsoft.com/v1.0/drives/b!xMpu9J3Jl06Z0b5hV3pMAu66u-T3rW5Gk94KImBvVaK6NtC_PGLeTIZdPJBGttur/items/01PMKS4KLKGQIVQSI6KJGKYR5P5N533Z5D/content' | jq .


curl -X GET --location -H "Authorization: Bearer $token" 'https://graph.microsoft.com/v1.0/drives/b!xMpu9J3Jl06Z0b5hV3pMAu66u-T3rW5Gk94KImBvVaK6NtC_PGLeTIZdPJBGttur/items/01PMKS4KLKGQIVQSI6KJGKYR5P5N533Z5D/content' -O
pandock -f docx content -t gfm -o content.md



https://hub.docker.com/r/pandoc/core
```bash
alias pandock=\
'docker run --rm -v "$(pwd):/data" -u $(id -u):$(id -g) pandoc/core'
```

https://www.tutorialsteacher.com/articles/convert-word-doc-to-markdown
`C:\pathToFile> pandoc myarticle.docx -o myarticle.md --extract-media=./images/`

https://stackoverflow.com/a/53139628/3356840
pandoc -f docx -t gfm somedoc.docx -o somedoc.md

