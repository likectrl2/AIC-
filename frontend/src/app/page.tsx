"use client";
import React, { useRef, useState } from "react";

interface CircuitData {
  projectId: string;
  projectName: string;
  [key: string]: any;
}

const CloseIcon = ({ className }: { className?: string }) => (
  <svg
    xmlns='http://www.w3.org/2000/svg'
    width='16'
    height='16'
    viewBox='0 0 24 24'
    fill='none'
    stroke='currentColor'
    strokeWidth='2.5'
    strokeLinecap='round'
    strokeLinejoin='round'
    className={className}
  >
    <line
      x1='18'
      y1='6'
      x2='6'
      y2='18'
    ></line>
    <line
      x1='6'
      y1='6'
      x2='18'
      y2='18'
    ></line>
  </svg>
);

export default function HomePage() {
  const [circuitData, setCircuitData] = useState<CircuitData | null>(null);
  const [message, setMessage] = useState<string>("");

  const fileInputRef = useRef<HTMLInputElement>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleUpdate = () => {
    fileInputRef.current?.click();
  };

  const handleDelete = () => {
    setSelectedFile(null);
    fileInputRef.current!.value = "";
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      setSelectedFile(file);
    }
  };

  return (
    <main className='flex h-full w-full flex-col items-center justify-center gap-3'>
      <div className='flex flex-col items-center justify-center'>
        <h1 className='text-7xl'>Untitled</h1>
        <h2 className='text-text-light text-2xl'>tste</h2>
      </div>
      <div className='flex h-10 w-[50%] rounded-sm outline-2 outline-blue-400 hover:outline-blue-500'>
        <input
          className='absolute h-0 w-0'
          type='file'
          ref={fileInputRef}
          onChange={(e) => {
            handleFileChange(e);
          }}
        />
        <label
          className='flex h-full w-full flex-1 p-1'
          onClick={selectedFile !== null ? () => {} : handleUpdate}
        >
          {selectedFile ? (
            <span className='mr-auto flex gap-1 rounded-sm p-1 hover:bg-blue-300 hover:outline-1 hover:outline-blue-500'>
              {selectedFile?.name}
              <span
                onClick={handleDelete}
                className='h-full'
              >
                <CloseIcon className='h-full hover:text-red-500' />
              </span>
            </span>
          ) : (
            "上传要转化的电路图"
          )}
        </label>
        <button className='aspect-square h-full rounded-sm bg-blue-400 hover:bg-blue-500'>{`\>`}</button>
      </div>
    </main>
  );
}
