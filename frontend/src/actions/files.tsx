'use server';

import { revalidatePath } from "next/cache";
import { unstable_noStore } from "next/cache";
import axios from "axios";
import { redirect } from "next/navigation";

const API = process.env.BACKEND_API


export async function uploadFile(jwToken : string | undefined, formData: FormData) {
    unstable_noStore();
    try {
      await axios.post(`${API}/api/file/`, formData, { headers: { 'Authorization': `Bearer ${jwToken}` } })
    } catch(error) {
      console.log(error)
      return;
    }
    redirect('/home');
}


export async function aUserUploadedFiles(jwToken : string, search: string) {
    unstable_noStore();
    try {
        if(search) {
          const { data } = await axios.get(`${API}/api/file/?search=${search}`, { headers: { 'Authorization': `Bearer ${jwToken}` } })
          return  data;
        } else {
          const { data } = await axios.get(`${API}/api/file/`, { headers: { 'Authorization': `Bearer ${jwToken}` } })
          return  data;
        }
    } catch(error) {
        console.log(error);
    }
}


export async function deleteFile(jwToken: string, fileId: string) {
    unstable_noStore();
    try {
      await axios.delete(`${API}/api/file/${fileId}`, { headers: { 'Authorization': `Bearer ${jwToken}` } }) 
    } catch(error) {
      console.log(error);
      return;
    }
    redirect('/home');
}
