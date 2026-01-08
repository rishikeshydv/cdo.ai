import React from 'react'
import { InfiniteSlider } from '@/components/motion-primitives/infinite-slider'
import Image from "next/image";
import { Button } from "@/components/ui/button";
import { cn } from '@/lib/utils'
import Link from 'next/link'
export default function Integration() {
  return (
    <div>
                <section>
            <div className=" py-24 md:py-32">
                <div className="mx-auto max-w-5xl px-6">
                    <div className="bg-muted/25 group relative mx-auto max-w-[22rem] items-center justify-between space-y-6 [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)] sm:max-w-md">
                        <div
                            role="presentation"
                            className="absolute inset-0 -z-10 bg-[linear-gradient(to_right,var(--color-border)_1px,transparent_1px),linear-gradient(to_bottom,#4f4f4f2e_1px,transparent_1px)] bg-[size:32px_32px] opacity-50"></div>
                        <div>
                            <InfiniteSlider
                                gap={24}
                                speed={20}
                                speedOnHover={10}>
                                <IntegrationCard>
                                    <Image src={"/algorand.svg"} alt="algorand" height={10} width={10}/>
                                </IntegrationCard>
                                <IntegrationCard>
                                    <Image src={"/firebase.svg"} alt="firebase" height={10} width={10}/>
                                </IntegrationCard>
                                <IntegrationCard>
                                    <Image src={"/gemini.svg"} alt="gemini" height={10} width={10}/>
                                </IntegrationCard>
                                <IntegrationCard>
                                   <Image src={"/n8n.svg"} alt="n8n" height={10} width={10}/>
                                </IntegrationCard>
                                <IntegrationCard>
                                    <Image src={"/nextjs_icon_dark.svg"} alt="nextjs_icon_dark" height={10} width={10}/>
                                </IntegrationCard>
                                <IntegrationCard>
                                    <Image src={"/qwik.svg"} alt="qwik" height={10} width={10}/>
                                </IntegrationCard>
                            </InfiniteSlider>
                        </div>

                        <div>
                            <InfiniteSlider
                                gap={24}
                                speed={20}
                                speedOnHover={10}
                                reverse>
                                <IntegrationCard>
                                    <Image src={"/algorand.svg"} alt="algorand" height={10} width={10}/>
                                </IntegrationCard>
                                <IntegrationCard>
                                    <Image src={"/firebase.svg"} alt="firebase" height={10} width={10}/>
                                </IntegrationCard>
                                <IntegrationCard>
                                    <Image src={"/gemini.svg"} alt="gemini" height={10} width={10}/>
                                </IntegrationCard>
                                <IntegrationCard>
                                   <Image src={"/n8n.svg"} alt="n8n" height={10} width={10}/>
                                </IntegrationCard>
                                <IntegrationCard>
                                    <Image src={"/nextjs_icon_dark.svg"} alt="nextjs_icon_dark" height={10} width={10}/>
                                </IntegrationCard>
                                <IntegrationCard>
                                    <Image src={"/qwik.svg"} alt="qwik" height={10} width={10}/>
                                </IntegrationCard>
                            </InfiniteSlider>
                        </div>
                        <div>
                            <InfiniteSlider
                                gap={24}
                                speed={20}
                                speedOnHover={10}>
                                <IntegrationCard>
                                    <Image src={"/algorand.svg"} alt="algorand" height={10} width={10}/>
                                </IntegrationCard>
                                <IntegrationCard>
                                    <Image src={"/firebase.svg"} alt="firebase" height={10} width={10}/>
                                </IntegrationCard>
                                <IntegrationCard>
                                    <Image src={"/gemini.svg"} alt="gemini" height={10} width={10}/>
                                </IntegrationCard>
                                <IntegrationCard>
                                   <Image src={"/n8n.svg"} alt="n8n" height={10} width={10}/>
                                </IntegrationCard>
                                <IntegrationCard>
                                    <Image src={"/nextjs_icon_dark.svg"} alt="nextjs_icon_dark" height={10} width={10}/>
                                </IntegrationCard>
                                <IntegrationCard>
                                    <Image src={"/qwik.svg"} alt="qwik" height={10} width={10}/>
                                </IntegrationCard>
                            </InfiniteSlider>
                        </div>
                        <div className="absolute inset-0 m-auto flex size-fit justify-center gap-2">
                            <IntegrationCard
                                className="shadow-black-950/10 size-16 bg-white/25 shadow-xl backdrop-blur-md backdrop-grayscale dark:border-white/10 dark:shadow-white/15"
                                isCenter={true}>
                                  <Image src={"/qwik.svg"} alt="qwik" height={10} width={10}/>
                            </IntegrationCard>
                        </div>
                    </div>
                    <div className="mx-auto mt-12 max-w-lg space-y-6 text-center">
                        <h2 className="text-balance text-3xl font-semibold md:text-4xl">Integrate with your favorite tools</h2>
                        <p className="text-muted-foreground">Connect seamlessly with popular platforms and services to enhance your workflow.</p>

                        <Button
                            variant="outline"
                            size="sm"
                            asChild>
                            <Link href="#">Get Started</Link>
                        </Button>
                    </div>
                </div>
            </div>
        </section>
    </div>
  )
}

const IntegrationCard = ({ children, className, isCenter = false }: { children: React.ReactNode; className?: string; position?: 'left-top' | 'left-middle' | 'left-bottom' | 'right-top' | 'right-middle' | 'right-bottom'; isCenter?: boolean }) => {
    return (
        <div className={cn('bg-background relative z-20 flex size-12 rounded-full border', className)}>
            <div className={cn('m-auto size-fit *:size-5', isCenter && '*:size-8')}>{children}</div>
        </div>
    )
}