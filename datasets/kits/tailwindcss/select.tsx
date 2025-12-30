import { Field, Label } from '@/components/fieldset'
import { Select } from '@/components/select'

function Example() {
  return (
    <Field>
      <Label>Project status</Label>
      <Select name="status">
        <option value="active">Active</option>
        <option value="paused">Paused</option>
        <option value="delayed">Delayed</option>
        <option value="canceled">Canceled</option>
      </Select>
    </Field>
  )
}