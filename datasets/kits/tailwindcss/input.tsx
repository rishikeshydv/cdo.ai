import { Field, Label } from '@/components/fieldset'
import { Input } from '@/components/input'

function Example() {
  return (
    <Field>
      <Label>Full name</Label>
      <Input name="full_name" />
    </Field>
  )
}