"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import Link from "next/link";

interface Article {
  id: number;
  title: string;
  slug: string;
}

export default function SearchPage() {
  const searchParams = useSearchParams();
  const query = searchParams.get("q") || "";

  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!query) return;

    async function fetchResults() {
      setLoading(true);
      try {
        const apiUrl = (typeof window !== "undefined" ? process.env.NEXT_PUBLIC_API_URL : "") || "";
        const res = await fetch(
          `${apiUrl}/api/search/?q=${encodeURIComponent(query)}`
        );
        if (!res.ok) throw new Error("Failed to fetch results");
        const data = await res.json();
        setArticles(data);
      } catch (err) {
        console.error("Error fetching search results:", err);
      } finally {
        setLoading(false);
      }
    }

    fetchResults();
  }, [query]);

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Search Results for: "{query}"</h1>

      {loading && <p>Loading...</p>}

      {!loading && articles.length === 0 && (
        <p className="text-gray-500">No results found.</p>
      )}

      <ul className="space-y-4">
        {articles.map((article) => (
          <li key={article.id}>
            <Link
              href={`/articles/${article.slug}`}
              className="text-blue-600 hover:underline"
            >
              {article.title}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
