import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { loginAccountThunk, createAccountThunk, resetState } from './account.slice';
import { loginAccountSchema, createAccountSchema } from "../../schemas/account.schema";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Card } from '../../components/ui/card';
import {
    Form,
    FormControl,
    // FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '../../components/ui/form';
import { Input } from '../../components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { ReloadIcon } from "@radix-ui/react-icons"
import { toast } from "sonner"
import { Button } from '../../components/ui/button';
import { useAuth } from '../../hooks/useAuth'
import { isEmpty, isNull } from 'lodash';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "../../components/ui/dropdown-menu"
import { SunIcon, MoonIcon } from "@radix-ui/react-icons"
import { useTheme } from 'next-themes';

const Login = () => {
    const { login } = useAuth();
    const dispatch = useDispatch();
    const { setTheme } = useTheme()
    const account = useSelector((state) => state.account.account);
    const status = useSelector((state) => state.account.status);
    const error = useSelector((state) => state.account.error);

    const loginAccountForm = useForm({
        resolver: zodResolver(loginAccountSchema),
        defaultValues: {
            email: "",
            password: "",
        },
    });

    const createAccountForm = useForm({
        resolver: zodResolver(createAccountSchema),
        defaultValues: {
            name: "",
            email: "",
            password: "",
        },
    });

    function handleLoginAccount(values) {
        dispatch(loginAccountThunk({ email: values.email, password: values.password }));
    }

    function handleCreateAccount(values) {
        dispatch(createAccountThunk({ name: values.name, email: values.email, password: values.password }));
    }

    useEffect(() => {
        if (status === "success" && !isEmpty(account)) {
            login({ 'cl-x-token': account.headers['cl-x-token'], 'cl-x-refresh': account.headers['cl-x-refresh'] });
            dispatch(resetState())
        }
    }, [account])

    useEffect(() => {
        if (!isNull(error)) {
            toast(JSON.stringify(error.error.message));
        }
    }, [error])

    return (
        <div className="flex flex-col h-screen w-full justify-center items-center p-4 gap-4">
            <div className="w-full h-20 p-4 rounded-md border">
                <div className='flex flex-row justify-between items-center'>
                    <div>TODO APP</div>
                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <Button variant="outline" size="icon">
                                <SunIcon className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
                                <MoonIcon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
                                <span className="sr-only">Toggle theme</span>
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                            <DropdownMenuItem onClick={() => setTheme("light")}>
                                Light
                            </DropdownMenuItem>
                            <DropdownMenuItem onClick={() => setTheme("dark")}>
                                Dark
                            </DropdownMenuItem>
                            <DropdownMenuItem onClick={() => setTheme("system")}>
                                System
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                </div>
            </div>
            <div className="flex h-screen w-full justify-center items-center">
                <Card className="p-8">
                    <Tabs defaultValue="login" className="w-[300px] md:w-[400px] lg:w-[600px]">
                        <TabsList>
                            <TabsTrigger value="login">Login</TabsTrigger>
                            <TabsTrigger value="signup">SignUp</TabsTrigger>
                        </TabsList>
                        <TabsContent value="login">
                            <Form {...loginAccountForm}>
                                <form onSubmit={loginAccountForm.handleSubmit(handleLoginAccount)} className="space-y-8">
                                    <FormField
                                        control={loginAccountForm.control}
                                        name="email"
                                        render={({ field }) => (
                                            <FormItem>
                                                <FormLabel>Email</FormLabel>
                                                <FormControl>
                                                    <Input placeholder="Email" {...field} />
                                                </FormControl>
                                                <FormMessage />
                                            </FormItem>
                                        )}
                                    />
                                    <FormField
                                        control={loginAccountForm.control}
                                        name="password"
                                        render={({ field }) => (
                                            <FormItem>
                                                <FormLabel>Password</FormLabel>
                                                <FormControl>
                                                    <Input placeholder="Password" type="password" {...field} />
                                                </FormControl>
                                                <FormMessage />
                                            </FormItem>
                                        )}
                                    />
                                    {status !== "loading" ?
                                        <Button type="submit">
                                            Login
                                        </Button> :
                                        <Button disabled>
                                            <ReloadIcon className="mr-2 h-4 w-4 animate-spin" />
                                            Please wait
                                        </Button>}
                                </form>
                            </Form>
                        </TabsContent>
                        <TabsContent value="signup">
                            <Form {...createAccountForm}>
                                <form onSubmit={createAccountForm.handleSubmit(handleCreateAccount)} className="space-y-8">
                                    <FormField
                                        control={createAccountForm.control}
                                        name="name"
                                        render={({ field }) => (
                                            <FormItem>
                                                <FormLabel>Name</FormLabel>
                                                <FormControl>
                                                    <Input placeholder="name" {...field} />
                                                </FormControl>
                                                <FormMessage />
                                            </FormItem>
                                        )}
                                    />
                                    <FormField
                                        control={createAccountForm.control}
                                        name="email"
                                        render={({ field }) => (
                                            <FormItem>
                                                <FormLabel>Email</FormLabel>
                                                <FormControl>
                                                    <Input placeholder="Email" {...field} />
                                                </FormControl>
                                                <FormMessage />
                                            </FormItem>
                                        )}
                                    />
                                    <FormField
                                        control={createAccountForm.control}
                                        name="password"
                                        render={({ field }) => (
                                            <FormItem>
                                                <FormLabel>Password</FormLabel>
                                                <FormControl>
                                                    <Input placeholder="Password" type="password" {...field} />
                                                </FormControl>
                                                <FormMessage />
                                            </FormItem>
                                        )}
                                    />
                                    {status !== 'loading' ?
                                        <Button type="submit">
                                            SignUp
                                        </Button> :
                                        <Button disabled>
                                            <ReloadIcon className="mr-2 h-4 w-4 animate-spin" />
                                            Please wait
                                        </Button>}
                                </form>
                            </Form>
                        </TabsContent>
                    </Tabs>
                </Card>
            </div>
        </div>
    );
};

export default Login;