import { useState, useEffect, useCallback } from "react";
import { DateRange } from "../services/api";

export function useAsync<T>(
  fetcher: () => Promise<T>,
  deps: any[]
): { data: T | null; loading: boolean; error: string | null; refetch: () => void } {
  const [data, setData]       = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState<string | null>(null);

  const fetch = useCallback(() => {
    setLoading(true);
    setError(null);
    fetcher()
      .then(setData)
      .catch((e) => setError(e.message ?? "Unknown error"))
      .finally(() => setLoading(false));
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  useEffect(() => { fetch(); }, [fetch]);

  return { data, loading, error, refetch: fetch };
}

export function useDateRange() {
  const [range, setRange] = useState<DateRange>({
    startDate: "2022-01-01",
    endDate:   new Date().toISOString().slice(0, 10),
  });

  return { range, setRange };
}
