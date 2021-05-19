library(readr)
library(dplyr)
library(stringr)
library(SwimmeR)


NYS <- read_csv("NYS_Full_Boys.csv")

NYS_Names <- NYS %>% 
  filter(is.na(Name) == FALSE,
         Meet %!in% c("Hilton 2019", "LISCA 2009")) %>% 
  select(Name) %>% 
  unique()

NYS_Names_Comma <- NYS_Names %>% 
  filter(str_detect(Name, ",") == TRUE) 

NYS_Names_Comma <- NYS_Names_Comma %>% 
  SwimmeR::name_reorder(verbose = TRUE) %>% 
  select(Name, First_Name) %>% 
  mutate(First_Name = str_remove(First_Name, "\\s[:alpha:]$")) %>% 
  mutate(First_Name = str_to_lower(First_Name))

NYS_Names_To_Add_1 <- NYS_Names_Comma %>%
  filter(First_Name %!in% Names_List) %>%
  select("X1" = First_Name) %>%
  unique() %>%
  arrange(X1) %>%
  filter(str_length(X1) > 1,
         str_detect(X1, "[:punct:]") == FALSE) %>%
  filter(
    X1 %!in% c(
      "aaaron",
      "aar",
      "aaro",
      "ad",
      "aj",
      "alba",
      "ale",
      "an",
      "andrew11",
      "anndrew",
      "anrdrew",
      "anth",
      "antho",
      "anthon",
      "anto",
      "at",
      "ath",
      "av",
      "ba",
      "ben rosen",
      "ben`",
      "bet",
      "bil",
      "bj",
      "bla",
      "blai",
      "bobb",
      "br",
      "bra",
      "brandon12",
      "br",
      "brittan",
      "brockport",
      "brya",
      "caitl",
      "calla",
      "calvin joh",
      "camer",
      "camero",
      "carrter",
      "carte",
      "catherin",
      "ce",
      "cef",
      "cha",
      "chandle",
      "charl",
      "charle",
      "chirs",
      "chr",
      "chri",
      "christai",
      "churchvill",
      "churchville",
      "cj",
      "clayto",
      "coleman grid",
      "colli",
      "colm",
      "conn",
      "conno",
      "courtne",
      "courtner",
      "crhistopher",
      "crist",
      "danie",
      "dav",
      "davi",
      "dean tana",
      "desmo",
      "diamanti",
      "dionici",
      "dj",
      "do",
      "domi",
      "domin",
      "domini",
      "domon",
      "dyla",
      "ebe",
      "edd",
      "eh ler",
      "eh super",
      "ej",
      "el",
      "elizab",
      "elizabe",
      "emm",
      "eri",
      "etha",
      "evav",
      "fed",
      "foste",
      "franci",
      "frankli",
      "gabrie",
      "garr",
      "garre",
      "geor",
      "georgin",
      "giu",
      "giusepp",
      "go",
      "goldberg",
      "gran",
      "gre",
      "greag",
      "grego",
      "grenville",
      "griffi",
      "guisepp",
      "ha",
      "ha sup",
      "hea",
      "heathe",
      "heung gyu",
      "hsa he doh",
      "huy houng",
      "ia",
      "irondequoi",
      "jae yoon",
      "jan hun",
      "jav",
      "jb",
      "jc",
      "jd",
      "je",
      "jea",
      "jean carlo",
      "jeffer",
      "jeffre",
      "jevont<U+FFFD>",
      "jin woo",
      "jj",
      "joesep",
      "joh",
      "joha",
      "john aden",
      "john lee",
      "john pet",
      "john peter",
      "john ross",
      "john tyler",
      "johnat",
      "johnn",
      "jon mike",
      "jona",
      "jonath",
      "jonatha",
      "jonathha",
      "jor",
      "jord",
      "jordn",
      "josef gera",
      "josh rober",
      "joshgua",
      "joshuah",
      "jp",
      "jt",
      "ju",
      "juan car",
      "juan carl",
      "juan rafae",
      "jung min",
      "jus",
      "jusitne",
      "justi",
      "ka",
      "kaitly",
      "katheri",
      "kathl",
      "kc",
      "ke",
      "keit",
      "kelse",
      "kenneth iv",
      ### through kerri
      "Madelei",
      "Meredit"
    )
  ) %>%
  mutate(str_replace(X1, "butter", "butterz")) %>%
  pull(X1)

write.csv(NYS_Names_To_Add_1, "NYS_Names_To_Add_1.csv")


NYS_Names_No_Comma <- NYS_Names %>% 
  filter(str_detect(Name, ",") == FALSE)

NYS_Names_No_Comma %>% 
  mutate(First_Name = case_when(str_count(Name, "\\s") > 2), str_remove_all(Name, ".*"))

Names <- read_csv("names.csv", col_names = FALSE)

Names_List <- unlist(Names)

names_2 <- bind_rows(Names, NYS_Names_To_Add_1)

#### notes
# aaaron
# butterz
