"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { Card, CardContent } from "../components/ui/card";
import {
  Leaf,
  MapPinned,
  Store,
} from "lucide-react";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";

// Hindi & English headings, points in English
const FeaturesSection = () => {
  const [mounted, setMounted] = useState(false);
  const { t } = useTranslation();

  useEffect(() => {
    setMounted(true);
  }, []);

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
      },
    },
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { duration: 0.6 } },
  };

  const features = [
    {
      icon: <Leaf className="h-8 w-8 text-green-600" />,
      title: "Fasal ka Rog (फ़सल का रोग)",
      points: [
        "Upload a crop photo to identify the specific disease quickly.",
        "Get detailed insights about the disease—its spread, symptoms, and causes.",
        "Receive two types of solutions: modern remedies (pesticides, chemicals) and home remedies (cow dung, neem, buttermilk, etc.)."
      ],
      route: "/DiseasePrediction"
    },
    {
      icon: <MapPinned className="h-8 w-8 text-blue-600" />,
      title: "Chitra Nirikshak (चित्र निरीक्षक)",
      points: [
        "Monitor the field using images taken from drones.",
        "Get exact coordinates of the diseased crops on your field map.",
        "Apply pesticides only to the infected areas for precise and efficient spraying."
      ],
      route: "/FieldAnalysis"
    },
    {
      icon: <Store className="h-8 w-8 text-orange-600" />,
      title: "Kisan Bazaar (किसान बाज़ार)",
      points: [
        "Platform for farmers to sell their produce directly to buyers.",
        "Farmers set their own prices for crops.",
        "Connect with buyers across India—no need to rely only on local markets."
      ],
      route: "/Marketplace"
    }
  ];

  return (
    <div className="relative py-24 px-4 sm:px-6 lg:px-8">
      <div className="absolute inset-0 overflow-hidden -z-10">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 rounded-full bg-green-500/5 blur-3xl"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full bg-blue-500/5 blur-3xl"></div>
      </div>

      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={mounted ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={mounted ? { opacity: 1, scale: 1 } : { opacity: 0, scale: 0.8 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="inline-block mb-4 px-4 py-1.5 rounded-full bg-gradient-to-r from-green-500/10 to-blue-500/10 backdrop-blur-sm border border-green-200/30 dark:border-green-700/30"
          >
            <span className="text-green-700 dark:text-green-400 font-medium text-sm">
              {t("KisanSaathi (किसानसाथी) — Smart Solutions for Farmers")}
            </span>
          </motion.div>
          <h2 className="text-3xl sm:text-4xl font-bold mb-4 text-slate-900 dark:text-white">
            {t("Key Features (मुख्य फीचर्स)")}
          </h2>
          <p className="text-slate-600 dark:text-slate-300 mb-12 max-w-2xl mx-auto text-lg">
            {t("Discover how technology is making your farming experience smarter!")}
          </p>
        </motion.div>

        <motion.div
          variants={container}
          initial="hidden"
          animate={mounted ? "show" : "hidden"}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
        >
          {features.map((feature, index) => (
            <motion.div key={index} variants={item}>
              <Link href={feature.route}>
                <Card className="overflow-hidden backdrop-blur-sm bg-white/80 dark:bg-slate-800/80 border border-slate-200/50 dark:border-slate-700/50 h-full hover:shadow-lg transition-shadow">
                  <CardContent className="p-6">
                    <motion.div
                      whileHover={{ scale: 1.05 }}
                      transition={{ type: "spring", stiffness: 300 }}
                      className="flex flex-col items-center text-center h-full"
                    >
                      <div className="mb-4 p-4 rounded-full bg-gradient-to-br from-green-100 to-blue-100 dark:from-green-900/30 dark:to-blue-900/30 shadow-md shadow-green-500/10">
                        {feature.icon}
                      </div>
                      <h3 className="text-xl font-semibold mb-3 text-slate-900 dark:text-white">
                        {feature.title}
                      </h3>
                      <ul className="text-slate-600 dark:text-slate-300 text-left mb-6 list-disc list-inside">
                        {feature.points.map((point, idx) => (
                          <li key={idx}>{point}</li>
                        ))}
                      </ul>
                    </motion.div>
                  </CardContent>
                </Card>
              </Link>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </div>
  );
};

export default FeaturesSection;