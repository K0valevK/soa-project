CREATE TABLE "user" (
  "id" integer PRIMARY KEY,
  "login" varchar
);

CREATE TABLE "task" (
  "id" integer PRIMARY KEY,
  "creator_id" integer,
  "like_num" integer,
  "view_num" integer
);

ALTER TABLE "task" ADD FOREIGN KEY ("creator_id") REFERENCES "user" ("id");
