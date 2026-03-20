export const useRoleGuard = () => {
    const { userRole, hasRole } = useAuth()
    const router = useRouter()

    const redirectBasedOnRole = () => {
        if (!userRole.value) {
            router.push('/login')
            return
        }

        if (hasRole('personal_limpieza')) {
            router.push('/cleaner-dashboard')
        } else if (hasRole('cliente')) {
            router.push('/client-dashboard')
        }
    }

    const guardRoute = (allowedRoles: string[]) => {
        if (!userRole.value) {
            router.push('/login')
            return false
        }

        if (!allowedRoles.includes(userRole.value)) {
            router.push('/unauthorized')
            return false
        }

        return true
    }

    return {
        redirectBasedOnRole,
        guardRoute
    }
}