---
layout: post
title:  "Planning a PC Build"
date:   2024-10-12
tags: draft
---

Earlier this year I built a so called "Small Form Factor" (SFF) PC. As the name suggests, these PCs priorize a smaller footprint and portibility compared to the typical more bulky desktops most people are familiar with. Browsing the popular [r/sffpc](https://www.reddit.com/r/sffpc/) you can see people showing off their SFF builds.

My build is not nearly as flashy or involved as many of the posts you'll find on that subreddit, but it was a fun project and I've been happy with the results. I thought I would write up a blog post describing the process of planning this build. This isn't intended to be a comprehensive guide on PC building, but you can refer to the references at the bottom for more guidance.

<!-- insert picture of build -->

I have almost exclusively used laptops in recent years and was unaware that building a desktop into such a small package was even possible. Laptops are conveniant and portable, but tend to have less powerful components and offer less flexibility with component selection and upgrades. For instance, the life of a desktop can often be extended with upgrades to the CPU, memory, or video card - often not possible with laptops. SFF PCs offer a compelling alternative if you want some of the advantages of a desktop without the extra bulk.

The PC I built is designed so that I can easily move it from one room to another. I could potentially even put it in a case or backpack and travel with it, but I don't see myself doing that in the near future. I had four purposes in mind when building the PC:

1. Typical PC gaming (connected to a monitor and usually using mouse and keyboard)
1. "Console-style" gaming (connected to a TV and using a controller)
1. Machine Learning work (Pytorch, Transformers)
1. Photo editing

All four of these use cases benefit from GPU (graphics card) acceleration so the graphics card was a priority. I also from the beginning planned to exclusively use Linux on the PC, which caused me to priotize an AMD graphics card for their driver support. People do use Nvidia graphics cards on Linux, but the driver support for AMD cards has historically been better from what I could tell.

### Planning

The first step in building a PC is to decide what you want to use it for and what your priorities are. For instance, a PC that is built for high performance gaming will likely require quite different components to PC intended for photo editing. Prioritizing a powerful graphics card makes sense for machine learning or gaming, but it may offer little benefit if the applications you intend to use don't heavily utilize graphics cards.

- What types of applications are you going to use it for?  
- What is your budget? 
- Does it need to be small and portable? 
- Is reducing fan noise a priority?

### Picking Components

[PCPartPicker Part List](https://pcpartpicker.com/list/NFjtdH)

Type|Item
:----|:----
**Case** | [S300 - Mini-ITX PC Gaming Case - Front I/O USB 3.0 Type - C Port - SFX Power Supply 100-130mm -Cable Management System - luminum Mini-ITX Motherboard Small Portable PC Case (PCIe 3.0 16X Rise](https://pcpartpicker.com/product/BtxRsY/placeholder) 
**Power Supply** | [Corsair SF750 (2018) 750 W 80+ Platinum Certified Fully Modular SFX Power Supply](https://pcpartpicker.com/product/nJrmP6/corsair-sf750-2018-750-w-80-platinum-certified-fully-modular-sfx-power-supply-cp-9020186-na) 
**Video Card** | [Sapphire PULSE Radeon RX 7700 XT 12 GB Video Card](https://pcpartpicker.com/product/TxTZxr/sapphire-pulse-radeon-rx-7700-xt-12-gb-video-card-11335-04-20g) 
**CPU** | [AMD Ryzen 5 7600 3.8 GHz 6-Core Processor](https://pcpartpicker.com/product/yXmmP6/amd-ryzen-5-7600-38-ghz-6-core-processor-100-100001015box) 
**CPU Cooler** | [ID-COOLING IS-55 Black 54.6 CFM CPU Cooler](https://pcpartpicker.com/product/7pjBD3/id-cooling-is-55-black-546-cfm-cpu-cooler-is-55-black) 
**Motherboard** | [ASRock A620I LIGHTNING WIFI Mini ITX AM5 Motherboard](https://pcpartpicker.com/product/zQhv6h/asrock-a620i-lightning-wifi-mini-itx-am5-motherboard-a620i-lightning-wifi)
**Wifi Adapter** | [Intel AX210 IEEE 802.11ax Bluetooth 5.2 Tri Band Wi-Fi/Bluetooth Combo Adapter for Notebook](https://pcpartpicker.com/product/khhFf7/placeholder)  
**Memory** | [G.Skill Flare X5 32 GB (2 x 16 GB) DDR5-6000 CL30 Memory](https://pcpartpicker.com/product/LBstt6/gskill-flare-x5-32-gb-2-x-16-gb-ddr5-6000-cl30-memory-f5-6000j3038f16gx2-fx5) 
**Storage** | [SK Hynix Platinum P41 2 TB M.2-2280 PCIe 4.0 X4 NVME Solid State Drive](https://pcpartpicker.com/product/yGTp99/sk-hynix-platinum-p41-2-tb-m2-2280-pcie-40-x4-nvme-solid-state-drive-shpp41-2000gm-2) 
**Case Fan** | [Noctua A12x15 PWM chromax.black.swap 55.44 CFM 120 mm Fan](https://pcpartpicker.com/product/FM3mP6/noctua-nf-a12x15-pwm-chromaxblackswap-5544-cfm-120-mm-fan-nf-a12x15-pwm-chromaxblackswap) 
 | Generated by [PCPartPicker](https://pcpartpicker.com) 2024-10-12 11:32 EDT-0400 |

- I selected the S300 case as it was a relatively inexpensive option (~$100) for a small (~8 Liter). Except for the front panel, the entire case is perforated metal so the airflow is quite good and helps keep components cooler than they otherwise would be in such a small case. I also considered the even smaller Velka 3 case, but this would have been more expensive, more of a process to build in, and greatly limited my options for graphics cards and CPU coolers. Two of the biggest considerations in an SFF build are the dimensions of CPU coolers and graphics cards that will fit in the case.
- The Ryzen 7600 CPU was selected for power efficiency.
- The 7700 XT GPU was a good value graphics card at the time of purchase. It outperforms the more expensive 4060 Ti from Nvidia.
- The ID-55 CPU cooler was the biggest cooler I could fit in this case. I also considered the AXP90-53 copper, but there were reports of difficulties mounting it on my motherboard of choice. I ended up swapping out the fan on the cooler for a quieter 12x120 mm Noctua fan, but this isn't necessary if you aren't too particular about fan noise.
- The Asrock A620i is one of the cheapest AM5 mini-itx motherboards around and it met all the requirements I needed. 

### References

- [How to Build A PC (Linus Tech Tips)](https://www.youtube.com/watch?v=s1fxZ-VWs2U). Very comprehensive video on all the steps of a PC build.
- [PC Part Picker](https://pcpartpicker.com/). Great resource for hardware compatibility checks on hardware and also looking at other builds that people have done.
- [Best Value GPU](https://bestvaluegpu.com/) - Track the best performance per dollar GPUs based on current prices
- [TechPowerUp.com](https://www.techpowerup.com/) - great detailed reviews of graphics cards and other products (ex. [RX 7700 XT Review](https://www.techpowerup.com/gpu-specs/radeon-rx-7700-xt.c3911)) 
- [Case End](https://caseend.com/) - detailed specs on PC cases
- Useful Subreddits:
    - [r/buildapc](https://www.reddit.com/r/buildapc/)
    - [r/buildmeapc](https://www.reddit.com/r/buildmeapc/)
    - [r/sffpc](https://www.reddit.com/r/sffpc/) - For small form factor (SFF) builds
    - [r/pcmasterrace](https://www.reddit.com/r/pcmasterrace/)

Youtube build videos are a great resource. I used the following video as a guide for my build: [S300 build $880 Lunchbox Gaming PC (1080p Destroyer)](https://www.youtube.com/watch?v=3BguJvWsyaM).

- [Building a Mid Range Gaming ITX PC doesn't have to be difficult - Featuring S300 ITX case](https://www.youtube.com/watch?v=rVP9kyrK7zk)
- [Don't Tell Big Rig Bros: This All AMD Small Foot Print Mini PC SLAYS AAA Games!](https://www.youtube.com/watch?v=0ypr8DxLKAE)
