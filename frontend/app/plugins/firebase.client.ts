import { initializeApp } from "firebase/app";
import { getAuth, onAuthStateChanged, getIdToken } from "firebase/auth";

export default defineNuxtPlugin(() => {
    const config = useRuntimeConfig().public.firebase
    const app = initializeApp(config)
    const auth = getAuth(app)

    const user = useState('user', () => null)
    const userRole = useState('userRole', () => null)

    onAuthStateChanged(auth, async (firebaseUser) => {
        if (firebaseUser) {
            try {
                const token = await getIdToken(firebaseUser, false)
                localStorage.setItem('auth_token', token)

                const userData = await $fetch('http://localhost:8000/users/me', {
                    headers: { Authorization: `Bearer ${token}` }
                })

                const idTokenResult = await firebaseUser.getIdTokenResult()
                const role = (idTokenResult.claims.role || 'cliente')

                user.value = {
                    uid: firebaseUser.uid,
                    email: firebaseUser.email,
                    displayName: userData.display_name
                }
                userRole.value = role
            } catch (error) {
                console.error('Error restoring auth state:', error)
                user.value = null
                userRole.value = null
                localStorage.removeItem('auth_token')
            }
        } else {
            user.value = null
            userRole.value = null
            localStorage.removeItem('auth_token')
        }
    })

    return {
        provide: {
            auth
        }
    }
})
