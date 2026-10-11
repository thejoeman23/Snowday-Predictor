"use client";

import { useParams } from "next/navigation";
import { useState, useEffect } from "react";

export default function Home() {
  const { slug: locationSlug } = useParams<{ slug: string }>();
  const [data, setData] = useState(null);

  useEffect(() => {
    // Fetch data
    fetch('https://api.snowyay.ca/predict?lat=44.56&lon=-80.904')
      .then(response => response.json())
      .then(data => setData(data));
  }, []);

  return (
    <div>
      <h1>{locationSlug}</h1>
      {data && <p>{JSON.stringify(data)}</p>}
    </div>
  );
} 

