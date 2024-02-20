from openai import OpenAI
client = OpenAI(api_key="")

# # logger.info(prompt)
# response = client.chat.completions.create(
#     model="gpt-3.5-turbo-0125",
#     messages=[
#         {"role": "system", "content": "You are an AI trained to translate from english to french"},
#         {"role": "user", "content": "Translate the following English text to French: 'Hello, how are you?' Please return the text in JSON format with an attribute for english and one for french"},
#     ],
#     response_format={"type","json_object"}
# )

# # Assuming the last message in the response is the review message
# review_message = response.choices[0].message.content.strip()
# print(review_message)

content = "Translate the following English text to French: 'Hello, how are you?' Please return the text in JSON format with an attribute for english and one for french"
# content = 'List of months that have 30 days in json'

# messages = [
#   {"role": "user", "content": content},
# ]
content = """Here is a sample code in React that fulfills the requirements:

import React, { useState } from 'react';

const UserForm = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    age: '',
    dob: '',
    gender: ''
  });
  const [error, setError] = useState('');
  const [responseMessage, setResponseMessage] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = () => {
    const { firstName, lastName, age, dob, gender } = formData;

    // Basic validation
    if (!firstName || !lastName || !age || !dob || !gender) {
      setError('All fields are required');
      return;
    } else {
      fetch('https://api.endpoint.com/users', {
        method: 'POST',
        body: JSON.stringify(formData),
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(response => response.json())
        .then(data => setResponseMessage(data.message))
        .catch(error => setError('An error occurred while posting data'));
    }
  };

  return (
    <div>
      <h1>User Information Form</h1>
      <input type="text" name="firstName" placeholder="First Name" onChange={handleChange} />
      <input type="text" name="lastName" placeholder="Last Name" onChange={handleChange} />
      <input type="number" name="age" placeholder="Age" onChange={handleChange} />
      <input type="date" name="dob" onChange={handleChange} />
      <select name="gender" onChange={handleChange}>
        <option value="">Select Gender</option>
        <option value="male">Male</option>
        <option value="female">Female</option>
        <option value="other">Other</option>
      </select>
      <button onClick={handleSubmit}>Submit</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {responseMessage && <p>{responseMessage}</p>}
    </div>
  );
};

export default UserForm;

In this code:

    The UserForm component renders a form with input fields for first name, last name, age, date of birth, and gender.
    The handleChange function tracks changes in the input fields and updates the form data state accordingly.
    The handleSubmit function checks for empty fields, posts the form data to the server if no errors are found, and displays the response message or error message to the user based on the server response.
    The form data is posted to a server endpoint using fetch API.
    The error state is used to display validation errors, and the responseMessage state is used to display the API response message.

You can further enhance this code by adding more validation logic, error handling, styling, and additional form fields as needed."""

prompt = f"""Review the following code snippet for quality and suggest improvements. You are an advocate for clean code. 
    The code should be clean and follow best practice programming patterns.  If improvements to the code can be made,
    describe the improvements to implement in the improvements attribute. The output should be the suggested improvements, you do not need to provide sample code. 
    If there are no new suggested improvements, the hasImprovements attribute should be false, otherwise it should be true.
    
    Please respond in json format with this structure:
    {{"improvements":"improvements go here","hasImprovements":"false"}}

    Here is the code:
    {content}"""

messages=[
        {"role": "system", "content": "You are an AI trained to review code for quality and suggest improvements."},
        {"role": "user", "content": prompt},
    ]

# client = OpenAI(api_key=userdata.get('OPENAI_API_KEY'))

response = completion = client.chat.completions.create(
  model="gpt-3.5-turbo-0125",
  messages=messages,
  response_format= { "type":"json_object" }
)

print(completion.choices[0].message.content)
