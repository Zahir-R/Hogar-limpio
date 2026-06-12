interface Toast {
  id: number
  message: string
  type: 'success' | 'error' | 'info'
}

let _id = 0

export function useToast() {
  const toasts = useState<Toast[]>('toasts', () => [])

  function show(message: string, type: Toast['type'] = 'info', duration = 3500) {
    const id = ++_id
    toasts.value.push({ id, message, type })
    setTimeout(() => remove(id), duration)
  }

  function remove(id: number) {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }

  function success(message: string) {
    show(message, 'success')
  }

  function error(message: string) {
    show(message, 'error', 5000)
  }

  function info(message: string) {
    show(message, 'info')
  }

  return { toasts, show, remove, success, error, info }
}
