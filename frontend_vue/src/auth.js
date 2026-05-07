import { reactive } from 'vue'

export const auth = reactive({
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  token: localStorage.getItem('token') || null,

  get isLoggedIn() {
    return !!this.token
  },

  get isProvider() {
    return this.user?.is_provider || false
  },

  get isAdmin() {
    return this.user?.is_staff || false
  },

  login(token, user) {
    this.token = token
    this.user = user
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(user))
  },

  logout() {
    this.token = null
    this.user = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },

  updateUser(userData) {
    this.user = { ...this.user, ...userData }
    localStorage.setItem('user', JSON.stringify(this.user))
  },
})
