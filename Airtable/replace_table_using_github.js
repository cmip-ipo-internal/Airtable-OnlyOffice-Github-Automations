/* 

Airtable template made for the CMIP-IPO
All queries: contact the IPO Technical Officer: 
Daniel Ellis
daniel.ellis -@- ext.esa.int

We replace a (institutes) table using the data from a github repository

*/
// GitHub repository information
const owner = 'cmip-ipo-internal';
const repo = 'MIPInstitutions';
const path = 'institutions.json'
// const githubToken = '******'; // Replace with your GitHub personal access token
const table_name = 'Institutes(automated)'


// Create a new GitHub issue

function getFileContents(owner, repo, path) {
    const apiUrl = `https://raw.githubusercontent.com/${owner}/${repo}/main/${path}`;;

    return fetch(apiUrl,{
      method: 'GET',
      headers: {
        'Authorization': `token ${githubToken}`,
        'Content-Type': 'application/json',
      }})
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .catch(error => {
            console.error('Error:', error);
            throw error;
        });
}

async function replaceTable(data){
    let table = base.getTable(table_name);

    // Step 1: Delete all existing records
    let existingRecords = await table.selectRecordsAsync();
    console.log(existingRecords)
    await table.deleteRecordsAsync(existingRecords['recordIds']);



    // Step 2: Parse data 
    let newRecordsData = [
        // Add new records here
        // {fields:{'col':val}}
    ];

    for (const [key, value] of Object.entries(data)) {
        if (value['indentifiers']!= undefined ) {
            let dummy = {
                'fields': {
                    'Name': key,
                    'LongName': value['indentifiers']['institution_name'],
                    'ROR': value['indentifiers']['ror']
                }
            };
            newRecordsData.push(dummy);
        }
    }

    console.log(newRecordsData)
    // Step 3: Insert new records
    await table.createRecordsAsync(newRecordsData);

    console.log("All records deleted and new records inserted.");

    }

await getFileContents(owner,repo,path).then(async (data)=>{if (data) await replaceTable(data)}).catch(err=>console.error(err))


