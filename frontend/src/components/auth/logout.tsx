import { logout } from "@/actions/auth";

export default function LogOut() {
    return (
        <>
            <form action={logout}>
                     <button className="logout" type="submit">Logout</button>
            </form>
        </>
    );
}