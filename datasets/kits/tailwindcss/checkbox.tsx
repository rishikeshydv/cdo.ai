import { Checkbox, CheckboxField, CheckboxGroup } from '@/components/checkbox'
import { Description, Fieldset, Label, Legend } from '@/components/fieldset'
import { Text } from '@/components/text'

function Example() {
  return (
    <Fieldset>
      <Legend>Discoverability</Legend>
      <Text>Decide where your events can be found across the web.</Text>
      <CheckboxGroup>
        <CheckboxField>
          <Checkbox name="discoverability" value="show_on_events_page" defaultChecked />
          <Label>Show on events page</Label>
          <Description>Make this event visible on your profile.</Description>
        </CheckboxField>
        <CheckboxField>
          <Checkbox name="discoverability" value="allow_embedding" />
          <Label>Allow embedding</Label>
          <Description>Allow others to embed your event details on their own site.</Description>
        </CheckboxField>
      </CheckboxGroup>
    </Fieldset>
  )
}