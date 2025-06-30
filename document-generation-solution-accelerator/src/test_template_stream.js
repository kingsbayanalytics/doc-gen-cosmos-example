// Test script to simulate frontend template request processing
async function testTemplateGeneration() {
  console.log('Testing template generation...');
  
  try {
    const response = await fetch('http://localhost:50505/history/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        messages: [
          {
            role: 'user',
            content: 'Create a simple workout plan template'
          }
        ],
        chat_type: 'template'
      })
    });

    if (!response.ok) {
      console.error('Response not OK:', response.status);
      return;
    }

    if (!response.body) {
      console.error('No response body');
      return;
    }

    console.log('Response OK, reading stream...');
    const reader = response.body.getReader();
    let runningText = '';
    let result = {};

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const text = new TextDecoder('utf-8').decode(value);
      console.log('Received chunk:', text.substring(0, 100) + '...');
      
      const objects = text.split('\n');
      objects.forEach(obj => {
        try {
          if (obj !== '' && obj !== '{}') {
            runningText += obj;
            result = JSON.parse(runningText);
            
            // Check the format that frontend expects
            if (!result.choices?.[0]?.messages?.[0]?.content) {
              console.error('Missing content in expected location');
              return;
            }
            
            console.log('✅ SUCCESS! Found content:', result.choices[0].messages[0].content.substring(0, 200) + '...');
            console.log('Template structure valid:', !!result.choices[0].messages[0].content.includes('template'));
            
            runningText = '';
          }
        } catch (e) {
          if (!(e instanceof SyntaxError)) {
            console.error('Parse error:', e);
          } else {
            console.log('Incomplete message, continuing...');
          }
        }
      });
    }

  } catch (error) {
    console.error('Test failed:', error);
  }
}

// Run the test
testTemplateGeneration().then(() => {
  console.log('Test completed');
}).catch(console.error);