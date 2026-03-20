import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  getIdToken,
  signOut as firebaseSignOut,
  updateProfile,
  type User
} from 'firebase/auth'
import { getId } from 'firebase/installations'

// Expected response from backend
interface UserMeResponse {
  uid: string
  email: string
  display_name?: string | null
}

interface UserData {
  uid: string
  email: string | null
  displayName?: string | null
}

interface LoginResult {
    user: UserData
    role: 'cliente' | 'personal_limpieza' | 'admin'
}

type UserRole = 'cliente' | 'personal_limpieza' | 'admin' | null

export const useAuth = () => {
  const { $auth } = useNuxtApp()
  const user = useState<UserData | null>('user', () => null)
  const userRole = useState<UserRole>('userRole', () => null)

  const login = async (email: string, pass: string): Promise<LoginResult | undefined> => {
    if (!import.meta.client) return

    try {
        const userCredential = await signInWithEmailAndPassword($auth, email, pass)

        const token = await getIdToken(userCredential.user, true)

        console.log(token)
        const userData = await $fetch<UserMeResponse>('http://localhost:8000/users/me', {
            headers: { Authorization: `Bearer ${token}` }
        })

        const idTokenResult = await userCredential.user.getIdTokenResult()
        const role = (idTokenResult.claims.role as 'cliente' | 'personal_limpieza' | 'admin') || 'cliente'

      
        user.value = {
            uid: userCredential.user.uid,
            email: userCredential.user.email,
            displayName: userData.display_name
        }
        userRole.value = role

        return { user: user.value, role }
    } catch (error) {
        console.error('Login error:', error)
        throw error
        }
    }

    const signup = async (
        email: string,
        pass: string,
        displayName: string,
        role: UserRole = 'cliente'
    ) => {
        try {
            const userCredential = await createUserWithEmailAndPassword($auth, email, pass)

            await updateProfile(userCredential.user, { displayName })

            const token = await getIdToken(userCredential.user)
            console.log(token)
            const syncResult = await $fetch('http://localhost:8000/users/signup-sync', {
                method: 'POST',
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: {
                    displayName: displayName,
                    role: role
                }
            })
        
            console.log('User synced with backend:', syncResult)
        
            await getIdToken(userCredential.user, true)
        
            const idTokenResult = await userCredential.user.getIdTokenResult()
            const userRoleClaim = (idTokenResult.claims.role as UserRole) || role
        
            user.value = {
                uid: userCredential.user.uid,
                email: userCredential.user.email,
                displayName: displayName
            }
            userRole.value = userRoleClaim
        
            return { user: user.value, role: userRoleClaim }
        } catch (error) {
            console.error('Signup error:', error)
            throw error
        }
    }

    const logout = async () => {
        try {
            await firebaseSignOut($auth)
            user.value = null
            userRole.value = null
            await navigateTo('/login')
        } catch (error) {
            console.error('Logout error:', error)
        }
    }

    const hasRole = (requiredRole: UserRole): boolean => {
        return userRole.value === requiredRole
    }

    const getToken = async (forceRefresh = false):  Promise<string | null> => {
        if (!import.meta.client) return null
        const auth = $auth
        if (!auth.currentUser) return null
        return await getIdToken(auth.currentUser, forceRefresh)
    }

    return {
        login,
        signup,
        logout,
        user,
        userRole,
        hasRole,
        getToken
    }
}