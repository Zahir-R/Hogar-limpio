import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

export default defineNuxtPlugin(() => {
    const config = useRuntimeConfig().public.firebase
    const app = initializeApp(config)
    const auth = getAuth(app)

    return {
        provide: {
            auth
        }
    }
})