"use client"
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import React from "react";
import axios from "axios"

type Props = {};

export default function UploadImage({}: Props) {
  const uploadImage=(e:React.ChangeEvent<HTMLInputElement>)=>{
    console.log(e.target.files[0])
    const formdata = new FormData();
    formdata.append("image", e.target.files[0])
    axios.post("https://divyanshurana312.pythonanywhere.com/predictions/predict/",formdata)
    .then((res)=>{
      console.log(res)
    })
  }

  return (
    <div className=" h-full overflow-auto">
      <div className="border-dashed border-2 p-12 flex flex-col justify-center items-center gap-4">
        <p className="text-[4rem] font-bold">Upload the Image</p>
        <p className="text-slate-500 text-center">
          Take your photos from blah to brilliant with our free online photo
          editor. Upload, edit, and share instantly from one place.
        </p>
        <div className="grid w-full max-w-sm items-center gap-1.5 relative">
          <input id="file" type="file" className="text-foregroundTemp hidden" onChange={uploadImage}/>
          <Label
            className="bg-backgroundTemp text-foregroundTemp p-4 text-center cursor-pointer"
            htmlFor="file"
          >
            Upload
          </Label>
        </div>
        <p className="text-slate-500"> or drop it here</p>
      </div>
    </div>
  );
}
