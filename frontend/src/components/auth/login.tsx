'use client';

import '../../styles/login.css';

import { useFormState } from "react-dom";
import { loginUser } from "@/actions/auth";
import Link from "next/link";

export default function LogIn() {
    const [state, loginAction] = useFormState(loginUser, undefined);

  return (
    <form autoComplete='off' className='forml' action={loginAction}>
      <div className="imgcontainer">
        <img src="https://www.w3schools.com/howto/img_avatar2.png" alt="Avatar" className="avatar" />
      </div>

      <div className="container">
        <label htmlFor="username"><b>Username</b></label>
        <input className='textl' type="text" placeholder="Enter Username" name="username" required />
        {state?.errors?.username && <p className="error">{state.errors.username}</p>}
    
        <label htmlFor="password"><b>Password</b></label>
        <input className='passl' type="password" placeholder="Enter Password" name="password" required />
        {state?.errors?.password && <p className="error">{state.errors.password}</p>}
    
        {state?.message && <p className="m-error" >{state.message}</p>}
        <button className='btnl' type="submit">Login</button>
      </div>
    
      <div className="container s_container">
        <span className="act">Do not have an account 🫡 ? <Link href="/signup">Register here</Link></span>
      </div>
    </form>
  );
}
