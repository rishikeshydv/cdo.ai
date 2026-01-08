import { Combobox, ComboboxLabel, ComboboxOption } from '@/components/combobox'
import { Field, Label } from '@/components/fieldset'

function Example({ currentUser, users }) {
  return (
    <Field>
      <Label>Assigned to</Label>
      <Combobox name="user" options={users} displayValue={(user) => user?.name} defaultValue={currentUser}>
        {(user) => (
          <ComboboxOption value={user}>
            <ComboboxLabel>{user.name}</ComboboxLabel>
          </ComboboxOption>
        )}
      </Combobox>
    </Field>
  )
}