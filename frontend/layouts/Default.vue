<script setup lang="ts">
import { ref } from 'vue'
import { useSidebar } from '../composables/useSidebar'
import Button from "@/components/Button.vue";

const { isOpen } = useSidebar()
const activeClass = ref(
    'bg-gray-600 bg-opacity-25 text-gray-100 border-gray-100',
)
const inactiveClass = ref(
    'border-gray-900 text-gray-500 hover:bg-gray-600 hover:bg-opacity-25 hover:text-gray-100',
)

const {
    data,
    status,
    signOut
} = useAuth();

</script>

<template>
    <nav class="fixed top-0 z-50 w-full border-b bg-gray-800 border-gray-700">
        <div class="px-3 py-3 lg:px-5 lg:pl-3">
            <div class="flex items-center justify-between flex flex-col lg:flex-row space-y-2 lg:space-y-0">
                <div class="flex items-center justify-center">
                    <a href="/" class="flex">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/c/c8/Logo_of_the_Technical_University_of_Munich.svg"
                            class="h-8 me-3" alt="TUM Logo" />
                        <span class="self-center text-xl font-semibold sm:text-2xl whitespace-nowrap text-white">
                            FinK Analytica
                        </span>
                    </a>
                </div>
                <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 font-medium space-x-5">
                    <Button link="/" text="Dashboard" />
                    <Button link="/db-management" text="Database Management" />
                    <Button link="/analysis" text="Text Analysis" />
                    <Button v-if="data && data.is_admin" link="/user-management" text="User Management" />
                </div>
                <div class="flex items-center">
                    <div v-if="status == 'authenticated'" class="flex items-center ms-3 text-white">
                        <div class="mx-2">{{ data && data.username }}</div>
                        <div class="my-1 text-base list-none divide-y rounded shadow bg-gray-700 divide-gray-600">
                            <ul class="py-1" role="none">
                                <li>
                                    <a href="#" class="block px-4 text-sm text-gray-300 hover:bg-gray-600 hover:text-white"
                                        role="menuitem" @click="signOut({ callbackUrl: '/' })">Sign out</a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </nav>
    <div class="p-4 pt-60 sm:pt-20 lg:pt-3">
        <div class="p-4 mt-14">
            <slot />
        </div>
    </div>
</template>
