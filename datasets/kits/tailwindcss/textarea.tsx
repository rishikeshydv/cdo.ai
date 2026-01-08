import { Field, Label } from '@/components/fieldset'
import { Textarea } from '@/components/textarea'

function Example() {
  return (
    <Field>
      <Label>Description</Label>
      <Textarea name="description" />
    </Field>
  )
}