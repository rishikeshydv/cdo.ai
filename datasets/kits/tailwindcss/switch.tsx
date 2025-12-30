import { Description, Label } from '@/components/fieldset'
import { Switch, SwitchField } from '@/components/switch'

function Example() {
  return (
    <SwitchField>
      <Label>Allow embedding</Label>
      <Description>Allow others to embed your event details on their own site.</Description>
      <Switch name="allow_embedding" defaultChecked />
    </SwitchField>
  )
}