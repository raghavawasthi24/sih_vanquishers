import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import Image from 'next/image'
import React from 'react'

type Props = {}

export default function Navbar({}: Props) {
  return (
    <div className="px-6 py-2 border border-b w-full flex flex-1 items-center">
       <div className=' flex flex-1 items-center'>
           <Image src="/MinistryofCoalLogo.svg" alt='logo' width={50} height={50}/>
           <p className='font-bold text-2xl ml-2'>Ministry Of Coal</p>
       </div>
       <Input
        type="search"
        placeholder="Search..."
        className="md:w-[100px] lg:w-[250px] bg-transparent"
      />


    </div>
  )
}