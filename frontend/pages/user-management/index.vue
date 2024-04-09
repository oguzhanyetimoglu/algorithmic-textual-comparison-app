<template>
    <div v-if="is_admin" class="container mx-auto p-4">
        <div class="flex space-x-16 items-center">
            <h1 class="text-4xl font-bold">User Management</h1>
            <button
                class="px-4 py-2 font-medium text-white bg-green-600 rounded-md hover:bg-green-500 focus:outline-none focus:shadow-outline-green active:bg-green-600 transition duration-150 ease-in-out"
                @click="showAddUserDialog = true">
                Add User
            </button>
        </div>
        <div v-if="showAddUserDialog" class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog"
            aria-modal="true">
            <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
                <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                <div
                    class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                    <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                        <div class="sm:flex sm:items-start">
                            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                                <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                                    Add User
                                </h3>
                                <div class="mt-2">
                                    <input type="text" v-model="newUser.username" placeholder="Username"
                                        class="block w-full p-2 border rounded-md">
                                    <input type="password" v-model="newUser.password" placeholder="Password"
                                        class="block w-full p-2 border rounded-md mt-2">
                                    <label class="flex items-center mt-2">
                                        <input type="checkbox" v-model="newUser.is_admin" class="form-checkbox">
                                        <span class="ml-2">Admin</span>
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                        <button type="button"
                            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm"
                            @click="addUser">
                            Add
                        </button>
                        <button type="button"
                            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                            @click="showAddUserDialog = false">
                            Cancel
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <table class="min-w-full divide-y divide-gray-200">
            <thead>
                <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Username</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="(user, index) in users" :key="index">
                    <td class="px-6 py-4 whitespace-nowrap">{{ user.username }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ user.is_admin ? 'Admin' : 'User' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                            :class="user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                            {{ user.is_active ? 'Active' : 'Inactive' }}
                        </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <button :disabled="!user.is_active"
                            class="px-4 py-2 font-medium text-white bg-blue-600 rounded-md hover:bg-blue-500 focus:outline-none focus:shadow-outline-blue active:bg-blue-600 transition duration-150 ease-in-out disabled:opacity-50 "
                            @click="editUser(user)">
                            Edit
                        </button>
                        <button :disabled="!user.is_active"
                            class="ml-2 px-4 py-2 font-medium text-white bg-red-600 rounded-md hover:bg-red-500 focus:outline-none focus:shadow-outline-red active:bg-red-600 transition duration-150 ease-in-out disabled:opacity-50 "
                            @click="confirmDeleteUser(user)">
                            Delete
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
        <div v-if="showEditUserDialog" class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title"
            role="dialog" aria-modal="true">
            <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
                <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                <div
                    class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                    <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                        <div class="sm:flex sm:items-start">
                            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                                <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                                    Edit User
                                </h3>
                                <div class="mt-2">
                                    <input type="text" v-model="userToEdit.username" placeholder="Username"
                                        class="block w-full p-2 border rounded-md">
                                    <input type="password" v-model="userToEdit.password" placeholder="Password"
                                        class="block w-full p-2 border rounded-md mt-2">
                                    <label class="flex items-center mt-2">
                                        <input type="checkbox" v-model="userToEdit.is_admin" class="form-checkbox">
                                        <span class="ml-2">Admin</span>
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                        <button type="button"
                            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm"
                            @click="updateUser">
                            Save
                        </button>
                        <button type="button"
                            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                            @click="showEditUserDialog = false">
                            Cancel
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div v-if="showDeleteUserDialog" class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog"
        aria-modal="true">
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
            <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
            <div
                class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                    <div class="sm:flex sm:items-start">
                        <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                            <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                                Confirm Delete
                            </h3>
                            <div class="mt-2">
                                <p>Are you sure you want to delete this user?</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                    <button type="button"
                        class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm"
                        @click="deleteUser(userToDelete.id)">Delete</button>
                    <button type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2
                        bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2
                        focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                        @click="showDeleteUserDialog = false">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    </div>
    <Notification v-if="notificationShow" :text="notificationText" :type="notificationType"
        @close="notificationShow = false" />
</template>




<script>
export default {
    data() {
        return {
            config: useRuntimeConfig(),
            token: '',
            is_admin: false,
            users: [],
            showAddUserDialog: false,
            showEditUserDialog: false,
            showDeleteUserDialog: false,
            userToDelete: null,
            newUser: {
                username: '',
                password: '',
                is_admin: false,
            },
            userToEdit: {
                id: null,
                username: '',
                password: '',
                is_admin: false,
            },
            notificationText: "",
            notificationType: "",
            notificationShow: false,
        };
    },
    async created() {
        const {
            token,
            data
        } = useAuth();
        this.token = token;
        this.is_admin = data.value.is_admin;
        const response = await fetch(`${this.config.public.apiBase}/auth/manage-user?limit=100`, {
            headers: {
                'Authorization': `${this.token}`,
            },
        });
        if (!response.ok) {
            throw new Error(`HTTP error! "created" status: ${response.status}`);
        }
        const tableData = await response.json();
        this.users = tableData.results;
    },
    methods: {
        async addUser() {
            const response = await fetch(`${this.config.public.apiBase}/auth/manage-user`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `${this.token}`,
                },
                body: JSON.stringify(this.newUser),
            });
            if (!response.ok) {
                this.notificationShow = true;
                this.notificationText = "User could not be added";
                this.notificationType = "danger";
                throw new Error(`HTTP error! "addUser" status: ${response.status}`);
            }
            const data = await response.json();
            data.password = '';
            this.users.push(data);
            this.showAddUserDialog = false;
            this.newUser = {
                username: '',
                password: '',
                is_admin: false,
            };
            this.notificationShow = true;
            this.notificationText = "User added successfully";
            this.notificationType = "success";
        },
        editUser(user) {
            this.userToEdit = { ...user };
            this.showEditUserDialog = true;
        },
        async updateUser() {
            const response = await fetch(`${this.config.public.apiBase}/auth/manage-user/${this.userToEdit.id}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `${this.token}`,
                },
                body: JSON.stringify(this.userToEdit),
            });
            if (!response.ok) {
                this.notificationShow = true;
                this.notificationText = "User could not be edited";
                this.notificationType = "danger";
                throw new Error(`HTTP error! "updateUser" status: ${response.status}`);
            }
            const data = await response.json();
            const index = this.users.findIndex(user => user.id === data.id);
            if (index !== -1) {
                this.users.splice(index, 1, data);
            }
            this.showEditUserDialog = false;
            this.userToEdit = {
                id: null,
                username: '',
                password: '',
                is_admin: false,
            };
            this.notificationShow = true;
            this.notificationText = "User updated successfully";
            this.notificationType = "success";
        },
        confirmDeleteUser(user) {
            this.userToDelete = user;
            this.showDeleteUserDialog = true;
        },
        async deleteUser(id) {
            const response = await fetch(`${this.config.public.apiBase}/auth/manage-user/${this.userToDelete.id}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `${this.token}`,
                },
            });
            if (!response.ok) {
                this.notificationShow = true;
                this.notificationText = "User could not be deleted";
                this.notificationType = "danger";
                throw new Error(`HTTP error! "deleteUser" status: ${response.status}`);
            }
            this.users = this.users.filter(user => user.id !== id);
            this.showDeleteUserDialog = false;
            this.notificationShow = true;
            this.notificationText = "User deleted successfully";
            this.notificationType = "success";
        },
    },
};
</script>