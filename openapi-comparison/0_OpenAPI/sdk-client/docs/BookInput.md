
# BookInput


## Properties

Name | Type
------------ | -------------
`title` | string
`author` | string

## Example

```typescript
import type { BookInput } from ''

// TODO: Update the object below with actual values
const example = {
  "title": null,
  "author": null,
} satisfies BookInput

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as BookInput
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


