# Testing Guide: Direct Model Access Feature

## Prerequisites

1. Install and run either:
   - **Ollama**: `ollama serve` (defaults to port 11434)
   - **LM Studio**: Start the local server (configure port as needed)

2. Pull a model in Ollama:
   ```bash
   ollama pull llama3
   ```

## Test Scenarios

### Test 1: Basic Direct Model Access (No Environment Variables)

1. Build and install the LibreOffice extension
2. Open LibreOffice Writer
3. Open the LibreThinker sidebar
4. You should see new controls:
   - [ ] Direct model access (checkbox)
   - Endpoint: http://localhost:11434/v1
   - Model: llama3
   - API Key (optional): (empty)

5. Check the "Direct model access" checkbox
6. Verify the three text fields become enabled
7. Type a prompt: "Write a haiku about coding"
8. Select some text or use entire document
9. Click Submit
10. Verify the response appears in the document

**Expected**: Response generated from local Ollama/LM Studio model

### Test 2: Environment Variables

1. Set environment variables before starting LibreOffice:
   ```bash
   export LT_DIRECT_ENABLED=1
   export LT_DIRECT_ENDPOINT=http://localhost:11434/v1
   export LT_DIRECT_MODEL=mistral
   export LT_DIRECT_API_KEY=your-key-here
   ```

2. Start LibreOffice and open the sidebar
3. Verify:
   - Checkbox is checked by default
   - Fields are populated with env var values
   - Fields are enabled

### Test 3: Toggle Checkbox

1. Open the sidebar
2. Check the "Direct model access" checkbox
3. Verify the three text fields are enabled
4. Uncheck the checkbox
5. Verify the three text fields are disabled/grayed out
6. Re-check the checkbox
7. Verify fields are enabled again

### Test 4: Error Handling - Server Not Running

1. Stop Ollama/LM Studio
2. Enable direct model access in the sidebar
3. Submit a prompt
4. Verify error message mentions checking if server is running

### Test 5: Error Handling - Invalid Model

1. Enable direct model access
2. Change model name to "nonexistent-model"
3. Submit a prompt
4. Verify error message with HTTP error details

### Test 6: Fallback to Original API

1. Uncheck "Direct model access" checkbox
2. Submit a prompt
3. Verify it uses the original librethinker.com API
4. Should see version update check in status

### Test 7: Empty Fields Validation

1. Enable direct model access
2. Clear the Endpoint field
3. Submit a prompt
4. Verify error: "Endpoint and Model fields are required"

### Test 8: Different Endpoints

Test with various endpoint formats:
- `http://localhost:11434/v1` (with /v1)
- `http://localhost:11434` (without /v1, should auto-append)
- `http://127.0.0.1:11434/v1`
- LM Studio: `http://localhost:1234/v1`

## Verification Checklist

- [ ] UI controls appear correctly in sidebar
- [ ] Checkbox enables/disables text fields
- [ ] Environment variables set default values
- [ ] Direct model access works with Ollama
- [ ] Direct model access works with LM Studio
- [ ] Error messages are clear and helpful
- [ ] Fallback to original API works when checkbox unchecked
- [ ] Field validation works
- [ ] Endpoint normalization works (auto-adds /v1)
- [ ] API key is sent when provided
- [ ] Response text inserts correctly into document

## Common Issues

### Issue: "Connection error"
**Solution**: Make sure Ollama/LM Studio is running and listening on the configured port

### Issue: "Invalid response format"
**Solution**: Verify the endpoint is OpenAI-compatible. Use `/v1/chat/completions` endpoint.

### Issue: UI controls don't appear
**Solution**: Rebuild the extension and verify installation

### Issue: Fields are disabled
**Solution**: Check the "Direct model access" checkbox

## Manual API Testing

Test the endpoint directly with curl:

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": false
  }'
```

Expected response:
```json
{
  "choices": [{
    "message": {"content": "Hello! How can I help you?"}
  }]
}
```
