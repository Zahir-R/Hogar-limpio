interface ConfirmState {
  visible: boolean
  title: string
  message: string
  resolve: ((value: boolean) => void) | null
}

export function useConfirm() {
  const state = useState<ConfirmState>('confirm-dialog', () => ({
    visible: false,
    title: '',
    message: '',
    resolve: null,
  }))

  function confirm(message: string, title = 'Confirmar acción'): Promise<boolean> {
    return new Promise((resolve) => {
      state.value = { visible: true, title, message, resolve }
    })
  }

  function accept() {
    state.value.resolve?.(true)
    state.value = { visible: false, title: '', message: '', resolve: null }
  }

  function cancel() {
    state.value.resolve?.(false)
    state.value = { visible: false, title: '', message: '', resolve: null }
  }

  return { state, confirm, accept, cancel }
}
