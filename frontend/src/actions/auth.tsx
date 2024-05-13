'use server';

import { LoginFormSchema, FormState, RegisterFormSchema } from "@/app/lib/definitions";
import { unstable_noStore } from "next/cache";
import { createSession, deleteSession } from "@/app/lib/session";
import { redirect } from "next/navigation";
import axios from "axios";

const API = process.env.BACKEND_API

export async function loginUser(state: FormState, formData: FormData) {
  unstable_noStore();
  // Validate form fields
  const validatedFields = LoginFormSchema.safeParse({
    username: formData.get('username'),
    password: formData.get('password'),
  })
  // If any form fields are invalid, return early
  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    }
  }
  try {
    const { data } = await axios.post(`${API}/api/token/`, validatedFields.data);
    const username = await userInfos(data.access);
    
    await createSession(data.access, data.refresh, username);

  } catch(error) {
    console.log(error);
    return {
      message: 'Invalid username or password',
    }
  }
  redirect('/home');
}


export async function userInfos(jwToken : string) {
    unstable_noStore();
    try {
      const { data } = await axios.get(`${API}/api/token/verify`, { headers: { 'Authorization': `Bearer ${jwToken}` } }) 
      return  data?.name;
      // await createSession(user?.name, user?.mail, user?.joinAt, user?.role);
      // redirect('/profile');
      // return data?.loggedUser
    } catch(error) {
      console.log(error);
      return null;
    }
}


export async function logout() {
  deleteSession();
  redirect('/signin');
}


export async function registerUser(state: FormState, formData: FormData) {
  unstable_noStore();
  // Validate form fields
  const validatedFields = RegisterFormSchema.safeParse({
    username: formData.get('username'),
    password1: formData.get('password'),
    password2: formData.get('passwordrepeat'),
    email: formData.get('email'),
    genre: formData.get('genre')
  })
  // If any form fields are invalid, return early errors
  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    }
  }

  const { username, password1, password2, email, genre } = validatedFields.data;
  // checking for passsword matching
  if(password1 != password2) {
    return {
      errors: {
        password2: 'Passwords must match',
      }
    }
  }

  try {
    const { data } = await axios.get(`${API}/username/?query=${username}`) 
    if(data === "taken") {
      return {
        errors: {
          username: 'Username already taken',
        }
      }
    }
    var response = await axios.get(`${API}/uregister/?username=${username}&password=${password1}&email=${email}&genre=${genre}`) ;
  } catch(error) {
    console.log(error);
    return {
      message: 'Oops...Something went wrong.',
    }
  }
  if(response.status === 201) {
    redirect('/signin');
  }
}
