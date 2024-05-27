import React, { useEffect, useState } from 'react';
import { useAuth } from '../../hooks/useAuth'
import { useSelector, useDispatch } from 'react-redux';
import { readAccountThunk, createTodoThunk, updateTodoThunk, readAllTodoThunk, deleteTodoThunk, resetState } from './todo.slice';
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "../../components/ui/card"
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
    DialogClose
} from "../../components/ui/dialog"
import { Badge } from "../../components/ui/badge"
import { Button } from '../../components/ui/button';
import { TrashIcon, Pencil2Icon, PlusIcon, SunIcon, MoonIcon, ExitIcon } from "@radix-ui/react-icons"
import { ScrollArea } from "../../components/ui/scroll-area"
import { Input } from "../../components/ui/input"
import {
    Pagination,
    PaginationContent,
    PaginationItem,
    PaginationLink,
    PaginationNext,
    PaginationPrevious,
} from "../../components/ui/pagination"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "../../components/ui/select"
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '../../components/ui/form';
import { isEmpty, isNull, size } from 'lodash';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { todoSchema } from '../../schemas/todo.schema';
import { todo_status } from '../../lib/utils';
import { toast } from "sonner"
import { useTheme } from 'next-themes';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "../../components/ui/dropdown-menu"

const Home = () => {
    const { setUser, logout, user } = useAuth();
    const { setTheme } = useTheme()
    const dispatch = useDispatch();

    const account = useSelector((state) => state.todo.account);
    const status = useSelector((state) => state.todo.status);
    const cud = useSelector((state) => state.todo.cud);
    const result = useSelector((state) => state.todo.result);
    const error = useSelector((state) => state.todo.error);
    const limit = 10

    const [page, setPage] = useState(1)
    const [filter, setFilter] = useState('All')
    const [items, setItems] = useState([])

    useEffect(() => {
        if (status === "success" && !isEmpty(account)) {
            setUser({ 'cl-x-token': account.headers['cl-x-token'], 'cl-x-refresh': account.headers['cl-x-refresh'] });
        }
    }, [account])

    useEffect(() => {
        if (status === "success" && !isEmpty(result)) {
            setUser({ 'cl-x-token': result.headers['cl-x-token'], 'cl-x-refresh': result.headers['cl-x-refresh'] });
            setItems(result.data.result)
            if (isEmpty(items) && page > 1) {
                setPage(page - 1)
            }
        }
    }, [result])

    useEffect(() => {
        if (status === "success" && !isEmpty(cud)) {
            setUser({ 'cl-x-token': cud.headers['cl-x-token'], 'cl-x-refresh': cud.headers['cl-x-refresh'] });
        }
    }, [cud])

    useEffect(() => {
        if (!isNull(error)) {
            toast(JSON.stringify(error.error.message));
        }
    }, [error])

    useEffect(() => {
        if (isEmpty(account) && isEmpty(result)) {
            dispatch(readAccountThunk({ user: user }))
            dispatch(readAllTodoThunk({ user: user, page: page, limit: limit }))
        }
    }, [])

    useEffect(() => {
        dispatch(readAllTodoThunk({ user: user, page: page, limit: limit, filter: filter }))
    }, [page, filter])

    const todoForm = useForm({
        resolver: zodResolver(todoSchema),
        defaultValues: {
            title: "",
            description: "",
        }
    })

    const handleUpdateTodo = (id) => async (values) => {
        await dispatch(updateTodoThunk({ user: user, id: id, title: values.title, description: values.description, status: values.status }))
        await dispatch(readAllTodoThunk({ user: user, page: page, limit: limit }))
        todoForm.reset()
    }

    const handleCreateTodo = async (values) => {
        await dispatch(createTodoThunk({ user: user, title: values.title, description: values.description, status: values.status }))
        await dispatch(readAllTodoThunk({ user: user, page: page, limit: limit }))
        todoForm.reset()
    }

    const handleDeleteTodo = async (id) => {
        await dispatch(deleteTodoThunk({ user: user, id: id }))
        await dispatch(readAllTodoThunk({ user: user, page: page, limit: limit }))
    }

    return (
        (isEmpty(account) && isEmpty(result) && isEmpty(items)) ? (<div>Loading...</div>) : (
            <div className="flex flex-col h-screen w-full justify-center items-center p-4 gap-4">
                <div className="w-full h-20 p-4 rounded-md border">
                    <div className='flex flex-row justify-between items-center'>
                        <div className='flex flex-col'>
                            <div>{account.data.result.name}</div>
                            <div>{account.data.result.email}</div>
                        </div>
                        <div className='flex flex-row justify-center items-center gap-4'>
                            <Dialog>
                                <DialogTrigger asChild>
                                    <Button>
                                        <PlusIcon className="h-4 w-4" />
                                    </Button>
                                </DialogTrigger>
                                <DialogContent>
                                    <DialogHeader>
                                        <DialogTitle>Create Todo</DialogTitle>
                                    </DialogHeader>
                                    <Form {...todoForm}>
                                        <form onSubmit={todoForm.handleSubmit(handleCreateTodo)} className="space-y-8">
                                            <div className='flex flex-col gap-4'>
                                                <FormField
                                                    control={todoForm.control}
                                                    name="title"
                                                    render={({ field }) => (
                                                        <FormItem>
                                                            <FormLabel>Title</FormLabel>
                                                            <FormControl>
                                                                <Input placeholder="Enter a title!" {...field} />
                                                            </FormControl>
                                                            <FormMessage />
                                                        </FormItem>
                                                    )}
                                                />
                                                <FormField
                                                    control={todoForm.control}
                                                    name="description"
                                                    render={({ field }) => (
                                                        <FormItem>
                                                            <FormLabel>Description</FormLabel>
                                                            <FormControl>
                                                                <Input placeholder="Enter a description" {...field} />
                                                            </FormControl>
                                                            <FormMessage />
                                                        </FormItem>
                                                    )}
                                                />
                                                <FormField
                                                    control={todoForm.control}
                                                    name="status"
                                                    render={({ field }) => (
                                                        <FormItem>
                                                            <FormLabel>Status</FormLabel>
                                                            <Select onValueChange={field.onChange} defaultValue={field.value}>
                                                                <FormControl>
                                                                    <SelectTrigger >
                                                                        <SelectValue placeholder="TODO" />
                                                                    </SelectTrigger>
                                                                </FormControl>
                                                                <SelectContent>
                                                                    {Object.values(todo_status).map((statusValue) => (
                                                                        <SelectItem key={statusValue} value={statusValue}>
                                                                            {statusValue}
                                                                        </SelectItem>
                                                                    ))}
                                                                </SelectContent>
                                                            </Select>
                                                            <FormMessage />
                                                        </FormItem>
                                                    )}
                                                />
                                            </div>
                                            <DialogClose asChild>
                                                <Button type="submit">
                                                    Create
                                                </Button>
                                            </DialogClose>
                                        </form>
                                    </Form>
                                </DialogContent>
                            </Dialog>
                            <Button variant="destructive" onClick={() => {
                                logout()
                                dispatch(resetState())
                            }}>
                                <ExitIcon className="h-4 w-4" />
                            </Button>
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
                </div>
                <div className='flex flex-col h-screen gap-4'>
                    <Select onValueChange={setFilter}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="All" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="All">All</SelectItem>
                            {Object.values(todo_status).map((statusValue) => (
                                <SelectItem key={statusValue} value={statusValue}>
                                    {statusValue}
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                    {isEmpty(items) ?
                        <div className='flex w-full h-screen rounded-md border p-4 justify-center items-center'>
                            <div className='text-center'>Sorry no more items!</div>
                        </div> :
                        <ScrollArea className="flex w-full h-full rounded-md border p-4 justify-center items-center">
                            <div className="grid grid-cols-1 gap-4 md:grid-cols-3 lg:grid-cols-5">
                                {items.map((item, index) => {
                                    return (
                                        <Card key={index}>
                                            <CardHeader>
                                                <Badge variant="outline" className="w-fit">{item.status}</Badge>
                                            </CardHeader>
                                            <CardContent className="flex flex-col gap-4">
                                                <CardTitle>{item.title}</CardTitle>
                                                <CardDescription>{item.description}</CardDescription>
                                            </CardContent>
                                            <CardFooter>
                                                <div className='flex flex-row gap-4'>
                                                    <Button variant="destructive" onClick={() => handleDeleteTodo(item.id)}>
                                                        <TrashIcon className="h-4 w-4" />
                                                    </Button>
                                                    <Dialog>
                                                        <DialogTrigger asChild>
                                                            <Button>
                                                                <Pencil2Icon className="h-4 w-4" />
                                                            </Button>
                                                        </DialogTrigger>
                                                        <DialogContent>
                                                            <DialogHeader>
                                                                <DialogTitle>Update Todo</DialogTitle>
                                                            </DialogHeader>
                                                            <Form {...todoForm}>
                                                                <form onSubmit={todoForm.handleSubmit(handleUpdateTodo(item.id))} className="space-y-8">
                                                                    <div className='flex flex-col gap-4'>
                                                                        <FormField
                                                                            control={todoForm.control}
                                                                            name="title"
                                                                            render={({ field }) => (
                                                                                <FormItem>
                                                                                    <FormLabel>Title</FormLabel>
                                                                                    <FormControl>
                                                                                        <Input placeholder={item.title} {...field} />
                                                                                    </FormControl>
                                                                                    <FormMessage />
                                                                                </FormItem>
                                                                            )}
                                                                        />
                                                                        <FormField
                                                                            control={todoForm.control}
                                                                            name="description"
                                                                            render={({ field }) => (
                                                                                <FormItem>
                                                                                    <FormLabel>Description</FormLabel>
                                                                                    <FormControl>
                                                                                        <Input placeholder={item.description} {...field} />
                                                                                    </FormControl>
                                                                                    <FormMessage />
                                                                                </FormItem>
                                                                            )}
                                                                        />
                                                                        <FormField
                                                                            control={todoForm.control}
                                                                            name="status"
                                                                            render={({ field }) => (
                                                                                <FormItem>
                                                                                    <FormLabel>Status</FormLabel>
                                                                                    <Select onValueChange={field.onChange} defaultValue={item.status}>
                                                                                        <FormControl>
                                                                                            <SelectTrigger>
                                                                                                <SelectValue placeholder={item.status} />
                                                                                            </SelectTrigger>
                                                                                        </FormControl>
                                                                                        <SelectContent>
                                                                                            {Object.values(todo_status).map((statusValue) => (
                                                                                                <SelectItem key={statusValue} value={statusValue}>
                                                                                                    {statusValue}
                                                                                                </SelectItem>
                                                                                            ))}
                                                                                        </SelectContent>
                                                                                    </Select>
                                                                                    <FormMessage />
                                                                                </FormItem>
                                                                            )}
                                                                        />
                                                                    </div>
                                                                    <DialogClose asChild>
                                                                        <Button type="submit">
                                                                            Update
                                                                        </Button>
                                                                    </DialogClose>
                                                                </form>
                                                            </Form>
                                                        </DialogContent>
                                                    </Dialog>

                                                </div>
                                            </CardFooter>
                                        </Card>)
                                })}
                            </div>
                        </ScrollArea>
                    }
                </div>
                <Pagination>
                    <PaginationContent>
                        <PaginationItem>
                            <PaginationPrevious href="#" onClick={() => {
                                if (page - 1 !== 0) {
                                    setPage(page - 1)
                                }
                            }} />
                        </PaginationItem>
                        <PaginationItem>
                            <PaginationLink href="#">{page}</PaginationLink>
                        </PaginationItem>
                        <PaginationItem>
                            <PaginationNext href="#" onClick={() => {
                                if (size(items) === limit) {
                                    setPage(page + 1)
                                }
                            }} />
                        </PaginationItem>
                    </PaginationContent>
                </Pagination>
            </div >
        ));
}
export default Home