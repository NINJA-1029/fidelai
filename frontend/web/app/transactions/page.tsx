"use client";

import { useState } from "react";
import { Table, TableHeader, TableHead, TableBody, TableRow, TableCell } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Search, Plus, Filter, ArrowDownRight, ArrowUpRight } from "lucide-react";

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
    description: "Monthly Salary - Tech Corp",
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
    <div className="space-y-6">
      <div className="flex justify-between items-center pb-4 border-b border-border">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Financial Ledger</h2>
          <p className="text-sm text-muted-foreground">
            Normalized transaction records across SMS, OCR receipts, and bank feeds
          </p>
        </div>
        <Button size="sm">
          <Plus className="w-4 h-4 mr-1.5" />
          Add Transaction
        </Button>
      </div>

      <div className="flex gap-4 items-center">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3 top-3 text-muted-foreground" />
          <Input
            placeholder="Search transactions by merchant, description, or category..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9"
          />
        </div>

        <div className="flex gap-2">
          {["all", "income", "housing", "groceries", "unexpected"].map((cat) => (
            <Button
              key={cat}
              variant={categoryFilter === cat ? "default" : "outline"}
              size="sm"
              onClick={() => setCategoryFilter(cat)}
              className="capitalize text-xs px-3"
            >
              {cat}
            </Button>
          ))}
        </div>
      </div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Transaction ID</TableHead>
            <TableHead>Date</TableHead>
            <TableHead>Description</TableHead>
            <TableHead>Category</TableHead>
            <TableHead>Ingestion Source</TableHead>
            <TableHead>Confidence</TableHead>
            <TableHead className="text-right">Amount</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {filtered.map((tx) => (
            <TableRow key={tx.id}>
              <TableCell className="font-mono text-xs text-muted-foreground">{tx.id}</TableCell>
              <TableCell className="font-mono text-xs">{tx.date}</TableCell>
              <TableCell className="font-medium">{tx.description}</TableCell>
              <TableCell>
                <Badge
                  variant={
                    tx.category === "Unexpected"
                      ? "destructive"
                      : tx.category === "Income"
                      ? "success"
                      : "outline"
                  }
                >
                  {tx.category}
                </Badge>
              </TableCell>
              <TableCell className="text-xs text-muted-foreground">{tx.source}</TableCell>
              <TableCell>
                <span className="text-xs font-mono">{Math.round(tx.confidence * 100)}%</span>
              </TableCell>
              <TableCell
                className={`text-right font-mono font-semibold ${
                  tx.type === "credit" ? "text-emerald-500" : "text-red-500"
                }`}
              >
                {tx.type === "credit" ? "+" : "-"}INR {tx.amount.toLocaleString("en-IN", { minimumFractionDigits: 2 })}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
