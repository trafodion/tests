# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# @@@ END COPYRIGHT @@@

cd call
javac *.java
jar -cvf ../call.jar *.class
rm *.class

cd ../spjrs
javac *.java
jar -cvf ../spjrs.jar *.class
rm *.class

cd ../dfr
javac *.java
jar -cvf ../dfr.jar *.class
rm *.class

cd ../dfr_rs
javac *.java
jar -cvf ../dfr_rs.jar *.class
rm *.class

cd ..
