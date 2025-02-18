/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_MANGA_BASE_URL: string;
  readonly VITE_VOLUME_PATH: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
