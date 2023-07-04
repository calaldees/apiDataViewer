https://developer.microsoft.com/en-us/graph/graph-explorer


curl -X GET -H "Authorization: Bearer $token" -H "Content-Type: application/json" https://graph.microsoft.com/v1.0/me/drive/recent | jq .

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

Top level graph paths
https://learn.microsoft.com/en-us/onedrive/developer/rest-api/?view=odsp-graph-online#microsoft-graph-root-resources
User    /v1.0/users/{id} or /v1.0/me
Group 	/v1.0/groups/{id}
Site 	/v1.0/sites/{id}



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


Accessing OneNote's shared with me
https://learn.microsoft.com/en-us/answers/questions/819677/use-onenote-api-to-get-notebooks-shared-with-me
https://graph.microsoft.com/v1.0/groups/%7Bgroup-id%7D/onenote/notebooks


I can find the oneNote id from url
https://cccu-my.sharepoint.com/personal/sm1161_canterbury_ac_uk/_layouts/15/Doc.aspx?sourcedoc={4e567f46-26e1-4d86-a276-85d21da712bd}&action=edit&wd=target%28Welcome.one%7Cdbead4cb-5ac6-44a0-88f7-675554363979%2FWelcome%20to%20Class%20Notebook%7Cb69048fc-b330-40d2-a7fe-18181ceff0d3%2F%29&wdorigin=NavigationUrl
{4e567f46-26e1-4d86-a276-85d21da712bd}



# me/drive/sharedWithMe

```python
{'@odata.type': '#microsoft.graph.driveItem',
'createdBy': {'user': {'displayName': 'Sharron MacKenzie',
                        'email': 'sm1161@canterbury.ac.uk',
                        'id': 'i:0#.f|membership|sm1161@canterbury.ac.uk'}},
'createdDateTime': '2022-09-12T17:29:08Z',
'file': {'hashes': {}, 'mimeType': 'application/octet-stream'},
'fileSystemInfo': {'createdDateTime': '2022-09-12T17:29:08Z',
                    'lastModifiedDateTime': '2022-12-07T12:27:22Z'},
'id': '01YFPQNPCGP5LE5YJGQZG2E5UF2IO2OEV5',
'lastModifiedBy': {'user': {'displayName': 'SharePoint App',
                            'id': 'i:0i.t|00000003-0000-0ff1-ce00-000000000000|app@sharepoint'}},
'lastModifiedDateTime': '2022-12-07T12:27:22Z',
'name': 'CCCU SD e-portfolio 22 - Computing',
'remoteItem': {'createdBy': {'user': {'displayName': 'Sharron '
                                                        'MacKenzie',
                                        'email': 'sm1161@canterbury.ac.uk',
                                        'id': 'i:0#.f|membership|sm1161@canterbury.ac.uk'}},
                'createdDateTime': '2022-09-12T17:29:08Z',
                'fileSystemInfo': {'createdDateTime': '2022-09-12T17:29:08Z',
                                    'lastModifiedDateTime': '2022-12-07T12:27:22Z'},
                'id': '01YFPQNPCGP5LE5YJGQZG2E5UF2IO2OEV5',
                'lastModifiedBy': {'user': {'displayName': 'SharePoint '
                                                            'App',
                                            'id': 'i:0i.t|00000003-0000-0ff1-ce00-000000000000|app@sharepoint'}},
                'lastModifiedDateTime': '2022-12-07T12:27:22Z',
                'name': 'CCCU SD e-portfolio 22 - Computing',
                'package': {'type': 'oneNote'},
                'parentReference': {'driveId': 'b!xHXgvoU8vEyzub0jAj4giVQZ349IKF1DmbUorCVrz_wXiqJtUlVZSbvdnNnEXbpC',
                                    'driveType': 'business',
                                    'id': '01YFPQNPF6Y2GOVW7725BZO354PWSELRRZ',
                                    'siteId': 'bee075c4-3c85-4cbc-b3b9-bd23023e2089'},
                'shared': {'scope': 'users',
                            'sharedBy': {'user': {'displayName': 'Sharron '
                                                                'MacKenzie',
                                                'email': 'sm1161@canterbury.ac.uk',
                                                'id': 'i:0#.f|membership|sm1161@canterbury.ac.uk'}},
                            'sharedDateTime': '2022-09-13T00:29:14Z'},
                'sharepointIds': {'listId': '6da28a17-5552-4959-bbdd-9cd9c45dba42',
                                    'listItemId': '23784',
                                    'listItemUniqueId': '4e567f46-26e1-4d86-a276-85d21da712bd',
                                    'siteId': 'bee075c4-3c85-4cbc-b3b9-bd23023e2089',
                                    'siteUrl': 'https://cccu-my.sharepoint.com/personal/sm1161_canterbury_ac_uk',
                                    'tenantId': '1b5e3164-426d-4946-95e1-4c156d541cda',
                                    'webId': '8fdf1954-2848-435d-99b5-28ac256bcffc'},
                'size': 0,
                'webDavUrl': 'https://cccu-my.sharepoint.com/personal/sm1161_canterbury_ac_uk/Documents/Class%20Notebooks/CCCU%20SD%20e-portfolio%2022%20-%20Computing',
                'webUrl': 'https://cccu-my.sharepoint.com/personal/sm1161_canterbury_ac_uk/_layouts/15/Doc.aspx?sourcedoc=%7B4E567F46-26E1-4D86-A276-85D21DA712BD%7D&file=CCCU%20SD%20e-portfolio%2022%20-%20Computing&action=edit&mobileredirect=true&wdorigin=Sharepoint'},
'size': 0,
'webUrl': 'https://cccu-my.sharepoint.com/personal/sm1161_canterbury_ac_uk/_layouts/15/Doc.aspx?sourcedoc=%7B4E567F46-26E1-4D86-A276-85D21DA712BD%7D&file=CCCU%20SD%20e-portfolio%2022%20-%20Computing&action=edit&mobileredirect=true&wdorigin=Sharepoint'},
```



OneNote - paths
https://learn.microsoft.com/en-us/graph/api/resources/onenote-api-overview?view=graph-rest-1.0&preserve-view=true


https://learn.microsoft.com/en-us/graph/api/sectiongroup-get?view=graph-rest-1.0&tabs=http
https://graph.microsoft.com/v1.0/users/c4168a74-5379-49f3-bda2-91efdd7a27d8/onenote/notebooks/1-c45f72e9-0b2b-4e65-a0d0-4c7d901749b7/sectionGroups/


https://learn.microsoft.com/en-us/graph/onenote-get-content#resource-paths-for-get-requests