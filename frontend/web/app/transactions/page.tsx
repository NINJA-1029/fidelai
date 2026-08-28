"use client";

import { useState } from "react";
import { Table, TableHeader, TableHead, TableBody, TableRow, TableCell } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const initialTransactions = [
  {
    id: "tx_demo_005",
    date: "2026-08-28",
    description: "Urgent Medical Treatment & Diagnostics",
    category: "Unexpected",
    source: "SMS Feed",
    type: "debit",
    amount: 12000.0,
    confidence: 0.98,
  },
  {
    id: "tx_demo_004",
    date: "2026-08-10",
    description: "Supermarket Weekly Provisions",
    category: "Groceries",
    source: "Receipt OCR",
    type: "debit",
    amount: 9000.0,
    confidence: 0.95,
  },
  {
    id: "tx_demo_003",
    date: "2026-08-05",
    description: "Electricity & Water Bill",
    category: "Utilities",
    source: "Bank API",
    type: "debit",
    amount: 2000.0,
    confidence: 1.0,
  },
  {
    id: "tx_demo_002",
    date: "2026-08-03",
    description: "Apartment Monthly Rent",
    category: "Housing",
    source: "Bank API",
    type: "debit",
    amount: 22000.0,
    confidence: 1.0,
  },
  {
    id: "tx_demo_001",
    date: "2026-08-01",
    description: "Monthly Salary — Tech Corp",
    category: "Income",
    source: "Bank API",
    type: "credit",
    amount: 65000.0,
    confidence: 1.0,
  },
];

export default function TransactionsPage() {
  const [search, setSearch] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("all");

  const filtered = initialTransactions.filter((tx) => {
    const matchesSearch =
      tx.description.toLowerCase().includes(search.toLowerCase()) ||
      tx.category.toLowerCase().includes(search.toLowerCase());
    const matchesCat = categoryFilter === "all" || tx.category.toLowerCase() === categoryFilter.toLowerCase();
    return matchesSearch && matchesCat;
  });

  return (
    <div className="space-y-[46px]">
      <div className="flex justify-between items-baseline pb-4 border-b border-border">
        <div>
          <span className="text-[11px] uppercase tracking-[0.18em] text-felt-gray block mb-1">
            03 // INGESTION LEDGER
          </span>
          <h2 className="text-[32px] md:text-[40px] font-light leading-[1.10] tracking-tight text-foreground">
            Financial Transactions
          </h2>
        </div>
        <span className="text-[11px] font-mono text-felt-gray uppercase">
          5 NORMALIZED RECORDS
        </span>
      </div>

      <div className="flex gap-4 items-center">
        <Input
          placeholder="Filter by description, merchant, or category..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1 font-mono text-[13px]"
        />

        <div className="flex gap-2">
          {["all", "income", "housing", "groceries", "unexpected"].map((cat) => (
            <Button
              key={cat}
              variant={categoryFilter === cat ? "default" : "outline"}
              size="sm"
              onClick={() => setCategoryFilter(cat)}
            >
              {cat.toUpperCase()}
            </Button>
          ))}
        </div>
      </div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="uppercase text-[11px] font-mono tracking-wider">Transaction ID</TableHead>
            <TableHead className="uppercase text-[11px] font-mono tracking-wider">Date</TableHead>
            <TableHead className="uppercase text-[11px] font-mono tracking-wider">Description</TableHead>
            <TableHead className="uppercase text-[11px] font-mono tracking-wider">Category</TableHead>
            <TableHead className="uppercase text-[11px] font-mono tracking-wider">Source</TableHead>
            <TableHead className="uppercase text-[11px] font-mono tracking-wider">Confidence</TableHead>
            <TableHead className="text-right uppercase text-[11px] font-mono tracking-wider">Amount</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {filtered.map((tx) => (
            <TableRow key={tx.id}>
              <TableCell className="font-mono text-[11px] text-felt-gray">{tx.id}</TableCell>
              <TableCell className="font-mono text-[12px]">{tx.date}</TableCell>
              <TableCell className="font-normal text-foreground">{tx.description}</TableCell>
              <TableCell>
                <Badge variant={tx.category === "Income" ? "solid" : "outline"}>
                  {tx.category.toUpperCase()}
                </Badge>
              </TableCell>
              <TableCell className="text-[11px] font-mono text-felt-gray">{tx.source}</TableCell>
              <TableCell className="font-mono text-[11px] text-felt-gray">
                {Math.round(tx.confidence * 100)}%
              </TableCell>
              <TableCell className="text-right font-mono font-medium text-foreground">
                {tx.type === "credit" ? "+" : "-"}INR {tx.amount.toLocaleString("en-IN", { minimumFractionDigits: 2 })}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
