import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    getIdToken
} from 'firebase/auth'

export const useAuth = () => {
    const { $auth } = useNuxtApp()
    const user = useState('user', () => null)

    const login = async (email: string, pass: string) => {
        if (!import.meta.client) return
        const userCredential = await signInWithEmailAndPassword($auth, email, pass)
        const token = await getIdToken(userCredential.user)

        const data = await $fetch('http://localhost:8000/users/me', {
            headers: { Authorization: `Bearer ${token}`}
        })

        return data
    }

    const signup = async (email: string, pass: string) => {
        const userCredential = await createUserWithEmailAndPassword($auth, email, pass)
        const token = await getIdToken(userCredential.user)

        const data = await $fetch('http://localhost:8000/users/signup-sync', {
            method: 'POST',
            headers: { Authorization: `Bearer ${token}` }
        })
        return data
    }

    return { login, signup, user }
}