/* 

Airtable template made for the CMIP-IPO
All queries: contact the IPO Technical Officer: 
Daniel Ellis
daniel.ellis -@- ext.esa.int

*/

// get the form result 
const inputCode = input.get("")

// Regular expression patterns to extract key-value pairs
const keyValuePattern = /<b>(.*?)<\/b><br\/>(.*?)<br\/><br\/><br\/>/g;
const keyPattern = /<b>(.*?)<\/b><br\/>/;
const valuePattern = /<br\/>(.*?)<br\/><br\/><br\/>/;

// Initialize an object to store key-value pairs
const result = {};

// Extract key-value pairs using regular expressions
let match;
while ((match = keyValuePattern.exec(inputCode)) !== null) {
  const keyMatch = keyPattern.exec(match[0]);
  const valueMatch = valuePattern.exec(match[0]);

  if (keyMatch && valueMatch) {
    const key = keyMatch[1];
    const value = valueMatch[1];
    result[key] = value.replace(/<[^>]*>/g, '');
  }
}

// Log the resulting JSON object
console.log(result);
