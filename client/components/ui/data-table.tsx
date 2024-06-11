import {
  flexRender,
  getFacetedRowModel,
  getFilteredRowModel,
  getSortedRowModel,
  SortingState,
  useReactTable,
} from "@tanstack/react-table";
import { ColumnDef, getCoreRowModel } from "@tanstack/table-core";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import React, { useState } from "react";
import { Input } from "@/components/ui/input";

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
}

export default function DataTable<TData, TValue>({
  columns,
  data,
}: DataTableProps<TData, TValue>) {
  const [sorting, setSorting] = useState<SortingState>([]);
  // const facets = column?.getFacetedUniqueValues();

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getFacetedRowModel: getFacetedRowModel(),

    state: {
      sorting,
    },
  });

  const columnFilteredValues = table.getColumn("status");

  return (
    <div className={"w-full"}>
      <div className="flex items-center py-4">
        <Input
          placeholder="Filter tasks..."
          value={
            (table.getColumn("scrap_query")?.getFilterValue() as string) ?? ""
          }
          onChange={(event) =>
            table.getColumn("scrap_query")?.setFilterValue(event.target.value)
          }
          className="max-w-sm"
        />
        {/*<DropdownMenu>*/}
        {/*  <DropdownMenuTrigger asChild>*/}
        {/*    <Button variant="outline" className="ml-auto">*/}
        {/*      Status <ChevronDown className="ml-2 h-4 w-4" />*/}
        {/*    </Button>*/}
        {/*  </DropdownMenuTrigger>*/}
        {/*  <DropdownMenuContent align="end">*/}
        {/*    {[...Object.values(ETaskStatus)].map((column) => {*/}
        {/*      return (*/}
        {/*        <DropdownMenuCheckboxItem*/}
        {/*          key={column.valueOf()}*/}
        {/*          className="capitalize"*/}
        {/*          checked={true}*/}
        {/*          // onCheckedChange={(value) => column.toggleVisibility(value)}*/}
        {/*        >*/}
        {/*          {column.valueOf()}*/}
        {/*        </DropdownMenuCheckboxItem>*/}
        {/*      );*/}
        {/*    })}*/}
        {/*  </DropdownMenuContent>*/}
        {/*</DropdownMenu>*/}
      </div>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext(),
                          )}
                    </TableHead>
                  );
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => {
                return (
                  <TableRow
                    key={row.id}
                    data-state={row.getIsSelected() && "selected"}
                  >
                    {row.getVisibleCells().map((cell) => (
                      <TableCell key={cell.id}>
                        {flexRender(
                          cell.column.columnDef.cell,
                          cell.getContext(),
                        )}
                      </TableCell>
                    ))}
                  </TableRow>
                );
              })
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      {/*<div className="flex items-center justify-end space-x-2 py-4">*/}
      {/*  <Button*/}
      {/*    variant="outline"*/}
      {/*    size="sm"*/}
      {/*    onClick={() => table.previousPage()}*/}
      {/*    disabled={!table.getCanPreviousPage()}*/}
      {/*  >*/}
      {/*    Previous*/}
      {/*  </Button>*/}
      {/*  <Button*/}
      {/*    variant="outline"*/}
      {/*    size="sm"*/}
      {/*    onClick={() => table.nextPage()}*/}
      {/*    disabled={!table.getCanNextPage()}*/}
      {/*  >*/}
      {/*    Next*/}
      {/*  </Button>*/}
      {/*</div>*/}
    </div>
  );
}
