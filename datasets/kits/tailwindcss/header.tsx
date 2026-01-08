import { Heading } from '@/components/heading'

function Example() {
  return (
    <div className="flex w-full flex-wrap items-end justify-between gap-4 border-b border-zinc-950/10 pb-6 dark:border-white/10">
      <Heading>Order #1011</Heading>
      <div className="flex gap-4">
        <Button outline>Refund</Button>
        <Button>Resend invoice</Button>
      </div>
    </div>
  )
}