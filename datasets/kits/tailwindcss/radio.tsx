import { Description, Fieldset, Label, Legend } from '@/components/fieldset'
import { Radio, RadioField, RadioGroup } from '@/components/radio'
import { Text } from '@/components/text'

function Example() {
  return (
    <Fieldset>
      <Legend>Resale and transfers</Legend>
      <Text>Decide if people buy tickets from you or from scalpers.</Text>
      <RadioGroup name="resale" defaultValue="permit">
        <RadioField>
          <Radio value="permit" />
          <Label>Allow tickets to be resold</Label>
          <Description>Customers can resell or transfer their tickets if they can’t make it to the event.</Description>
        </RadioField>
        <RadioField>
          <Radio value="forbid" />
          <Label>Don’t allow tickets to be resold</Label>
          <Description>Tickets cannot be resold or transferred to another person.</Description>
        </RadioField>
      </RadioGroup>
    </Fieldset>
  )
}